import os
import re
import xml.etree.ElementTree as ET
from html import unescape
from dotenv import dotenv_values
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, green, gray, black
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import textwrap
import pandas as pd
from tabulate import tabulate

STATUS_COLOR = {
    'PASS': green,
    'FAIL': red,
    'NOT RUN': gray,
}

def extrair_info_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    robot_info = root.attrib
    suite = root.find('suite')
    suite_name = suite.attrib.get('name', 'Desconhecido') if suite is not None else 'N/A'
    return {
        'suite_name': suite_name,
        'generated': robot_info.get('generated', 'N/A'),
        'generator': robot_info.get('generator', 'N/A'),
        'root': root
    }

def extrair_fluxo(element, test_name):
    resultado = []
    for kw in element.findall('kw'):
        name = unescape(kw.attrib.get('name', ''))
        owner = kw.attrib.get('owner', '')

        if owner == 'keywords' and name.strip().startswith("Gerar evidencia"):
            continue

        status_el = kw.find('status')
        status = status_el.attrib.get('status', 'PASS') if status_el is not None else 'PASS'
        msg_el = kw.find('msg')
        time = msg_el.attrib.get('time') if msg_el is not None else '9999-99-99T99:99:99.999'

        args = [unescape(arg.text or '') for arg in kw.findall('arg')]
        argumentos_formatados = f" {args}" if args else ""
        nome_completo = name + argumentos_formatados

        entrada = {
            'test_name': test_name,
            'name': nome_completo,
            'owner': owner,
            'status': status,
            'time': time,
            'screenshot': None,
        }

        for subkw in kw.findall('.//kw'):
            if subkw.attrib.get('owner') == 'Browser' and subkw.attrib.get('name') == 'Take Screenshot':
                msg_sub = subkw.find('msg')
                if msg_sub is not None:
                    match = re.search(r'(?:href|src)="(browser/screenshot/[^"]+)"', msg_sub.text or '')
                    if match:
                        entrada['screenshot'] = unescape(match.group(1))

        resultado.append(entrada)
        resultado.extend(extrair_fluxo(kw, test_name))
    return resultado

def desenhar_capa(c, infos, logos, env):
    width, height = A4
    margin = 2 * cm
    logo_max_width = 3 * cm
    logo_top_y = A4[1] - 1.5 * cm

    if os.path.exists(logos['rge']):
        img_rge = ImageReader(logos['rge'])
        iw, ih = img_rge.getSize()
        scale = logo_max_width / iw
        final_width = iw * scale
        final_height = ih * scale
        c.drawImage(img_rge, margin, logo_top_y - final_height, width=final_width, height=final_height, mask='auto')

    if os.path.exists(logos['cpfl']):
        img_cpfl = ImageReader(logos['cpfl'])
        iw, ih = img_cpfl.getSize()
        scale = logo_max_width / iw
        final_width = iw * scale
        final_height = ih * scale
        c.drawImage(img_cpfl, A4[0] - margin - final_width, logo_top_y - final_height, width=final_width, height=final_height, mask='auto')

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 6 * cm, "EVIDÊNCIAS DE QUALIDADE")

    c.setFont("Helvetica", 12)
    y = height - 8 * cm
    spacing = 1.1 * cm

    y -= spacing
    c.drawString(margin, y, f"DATA E HORA DO TESTE: {infos['generated']}")
    y -= spacing
    c.drawString(margin, y, f"PLATAFORMA/TECNOLOGIA: {infos['generator']}")
    y -= spacing
    c.line(margin, y, width - margin, y)
    y -= spacing * 0.5
    c.drawString(margin, y, f"TÍTULO DO PROJETO: {env.get('NOME_PROJETO', 'Não informado')}")
    y -= spacing
    c.drawString(margin, y, f"GERENTE DO PROJETO: {env.get('NOME_GERENTE', 'Não informado')}")
    y -= spacing
    c.drawString(margin, y, f"SPONSOR DO PROJETO: {env.get('NOME_SPONSOR', 'Não informado')}")
    y -= spacing
    c.drawString(margin, y, f"VP e DIRETORIA: {env.get('NOME_DIRETORIA_VP', 'Não informado')}")
    c.showPage()

def desenhar_sumario(c, testes):
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(A4[0]/2, A4[1] - 3*cm, "SUMÁRIO")
    y = A4[1] - 5*cm
    c.setFont("Helvetica", 12)

    for idx, nome in enumerate(testes, 1):
        if y < 3*cm:
            c.showPage()
            y = A4[1] - 3*cm
        c.drawString(3*cm, y, f"{idx}. {nome}")
        y -= 1.0 * cm
    # c.showPage()    #Estava gerando uma pagina vazia

def desenhar_texto_quebrado(c, text, x, y, max_width, font="Helvetica", font_size=10, line_spacing=14, color=black):
    c.setFont(font, font_size)
    c.setFillColor(color)
    max_chars_per_line = int(max_width / (font_size * 0.6))
    linhas = textwrap.wrap(text, width=max_chars_per_line)

    for linha in linhas:
        if y < 50:
            c.showPage()
            y = A4[1] - 2 * cm
            c.setFont(font, font_size)
            c.setFillColor(color)

        c.drawString(x, y, linha)
        y -= line_spacing

    return y

def coletar_testes_e_evidencias(root, pasta_screenshots):
    todas_entradas = []
    testes_encontrados = []

    for test in root.findall('.//test'):
        nome_teste = test.attrib.get('name', 'Sem nome')
        if nome_teste not in testes_encontrados:
            testes_encontrados.append(nome_teste)
        todas_entradas.extend(extrair_fluxo(test, nome_teste))

    todas_entradas.sort(key=lambda x: x['time'])
    return testes_encontrados, todas_entradas

def desenhar_evidencias(c, todas_entradas, pasta_screenshots):
    width, height = A4
    margin = 2 * cm
    y = height - margin
    spacing = 14

    ultimo_teste = None
    for entrada in todas_entradas:
        if entrada['owner'] != 'keywords':
            continue

        if entrada['test_name'] != ultimo_teste:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(black)
            c.drawString(margin, y, f"Teste: {entrada['test_name']}")
            y -= spacing * 2  # 2 linhas de espaço
            ultimo_teste = entrada['test_name']

        cor = STATUS_COLOR.get(entrada['status'], black)
        y = desenhar_texto_quebrado(
            c,
            text=entrada['name'],
            x=margin,
            y=y,
            max_width=width - 2 * margin,
            font="Helvetica",
            font_size=10,
            color=cor
        )
        y -= spacing * 0.5

        img_path = None
        if entrada['screenshot']:
            img_path = os.path.join(pasta_screenshots, os.path.basename(entrada['screenshot']))
        elif entrada['status'] == 'FAIL':
            img_path = os.path.join(pasta_screenshots, "fail-screenshot-1.png")

        if img_path and os.path.exists(img_path):
            try:
                img = ImageReader(img_path)
                iw, ih = img.getSize()
                scale = min(12 * cm / iw, 6 * cm / ih)
                iw *= scale
                ih *= scale

                if y - ih < margin:
                    c.showPage()
                    y = height - margin

                border_color = (0.68, 0.85, 0.90)
                if "fail" in os.path.basename(img_path).lower():
                    border_color = (1, 0, 0)

                border_padding = 2
                c.setStrokeColorRGB(*border_color)
                c.setLineWidth(2)
                x_centralizado = (width - iw) / 2
                # c.rect(margin - border_padding, y - ih - border_padding, iw + 2 * border_padding, ih + 2 * border_padding)
                c.rect(x_centralizado - border_padding, y - ih - border_padding, iw + 2 * border_padding, ih + 2 * border_padding)


                # c.drawImage(img, margin, y - ih, width=iw, height=ih)

                c.drawImage(img, x_centralizado, y - ih, width=iw, height=ih)
                y -= ih + spacing * 2
            except Exception as e:
                c.setFont("Helvetica-Oblique", 9)
                c.setFillColor(red)
                c.drawString(margin, y, f"[Erro ao carregar imagem: {e}]")
                y -= spacing
        elif img_path:
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColor(red)
            c.drawString(margin, y, f"[Imagem não encontrada: {img_path}]")
            y -= spacing

def desenhar_massa_de_dados(c, caminho_csv):
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(A4[0]/2, A4[1] - 3*cm, "MASSA DE DADOS")
    y = A4[1] - 5*cm
    try:
        df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8")
        texto = tabulate(df, headers='keys', tablefmt='plain', showindex=False)
        linhas = texto.split('\n')
        c.setFont("Courier", 9)
        for linha in linhas:
            if y < 3*cm:
                c.showPage()
                y = A4[1] - 3*cm
                c.setFont("Courier", 9)
            c.drawString(2*cm, y, linha)
            y -= 12
        c.showPage()
    except Exception as e:
        c.setFont("Helvetica-Oblique", 12)
        c.setFillColor(red)
        c.drawString(2*cm, y, f"Erro ao carregar a massa de dados: {e}")
        c.showPage()

def gerar_relatorio_pdf(xml_path, env_path, screenshot_dir, pdf_saida):
    infos = extrair_info_xml(xml_path)
    env = dotenv_values(env_path)
    c = canvas.Canvas(pdf_saida, pagesize=A4)

    # [1] Capa
    desenhar_capa(c, infos, {
        'rge': os.path.join('imagens', 'logoRGE.png'),
        'cpfl': os.path.join('imagens', 'logoCPFL.png'),
    }, env)

    # [2] Coletar informações dos testes e evidências
    testes_encontrados, todas_entradas = coletar_testes_e_evidencias(infos['root'], screenshot_dir)

    # [3] Sumário na página 2
    desenhar_sumario(c, testes_encontrados)

    # [4] Evidências
    desenhar_evidencias(c, todas_entradas, screenshot_dir)

    # [5] Massa de dados
    caminho_massa = os.path.join('resources', 'data', 'massa.csv')
    desenhar_massa_de_dados(c, caminho_massa)

    # [6] Salvar o PDF
    c.save()
    print(f"✅ PDF final gerado com capa, sumário, evidências e massa de dados: {pdf_saida}")

# === EXECUTAR ===
if __name__ == "__main__":
    gerar_relatorio_pdf(
        xml_path="output.xml",
        env_path=".env",
        screenshot_dir="browser/screenshot",
        pdf_saida="relatorio_final.pdf"
    )