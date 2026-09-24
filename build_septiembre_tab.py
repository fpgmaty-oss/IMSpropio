"""
build_septiembre_tab.py
------------------------
Regenera la pestana "Categorias Sept" (analisis de categorias MTD por local)
dentro de index.html, a partir de un reporte HTML fuente (el que genera el
export de Power BI + code-puppy, tipo "Analisis Categorias <Mes> <Anio> -
<Local>.html").

Uso:
    python build_septiembre_tab.py "C:\\ruta\\al\\reporte_categorias.html"

Si no se pasa ruta, usa la ultima usada (ver REPORT_PATH_DEFAULT abajo).

Que hace:
1. Parsea la tabla "Resumen Completo por Categoria" del reporte fuente.
2. Calcula Top 3 Positivos / Top 3 Negativos por Impacto $ (mismo criterio
   que ya usa el reporte fuente en su resumen ejecutivo).
3. Genera el bloque JS (datos + funcion de render) y lo inyecta/reemplaza
   dentro de index.html, sin tocar el resto del archivo.

Nota: los datos quedan "horneados" (estaticos) dentro del HTML, igual que la
Maestra y el resto de la app. Si llega un reporte nuevo (otro mes u otro
local), correr este script de nuevo con la ruta nueva.
"""

import json
import re
import sys
from pathlib import Path

REPORT_PATH_DEFAULT = (
    r"C:\Users\m0s0rvl\OneDrive - Walmart Inc\Escritorio"
    r"\Analisis Categorias Septiembre 2026 - San Javier #155 (1).html"
)
INDEX_PATH = Path(__file__).parent / "index.html"

BLOCK_START = "        // ---- Analisis de Categorias Septiembre 2026 (San Javier #155) ----"
BLOCK_END_MARKER = "\n        function populateSalesFilters() {"
ANCHOR_FALLBACK = "            applySalesFilters();\n        }\n"


def to_millions(s):
    m = re.search(r"-?\d+\.?\d*", s.replace(",", "."))
    return float(m.group(0)) if m else 0.0


def to_pct(s):
    m = re.search(r"-?\d+\.?\d*", s)
    return float(m.group(0)) if m else 0.0


def strip_tags(s):
    return re.sub("<[^>]+>", "", s).strip()


def extract_meta(html):
    """Saca los KPIs de cabecera del reporte fuente via regex simples."""
    def grab(pattern, default=None, cast=str):
        m = re.search(pattern, html, re.S)
        return cast(m.group(1)) if m else default

    local = grab(r'<div class="subtitle">Local (.*?) ·', "Local desconocido")
    fuente = grab(r"Fuente: (.*?)</div>", "Fuente desconocida")
    corte = grab(r"Corte (.*?)\.", "Corte desconocido")
    venta_mtd = grab(r"Venta MTD.*?kpi-value[^>]*>\$([\d.]+)M", cast=float)
    venta_ly = grab(r"LY: \$([\d.]+)M", cast=float)
    var_pct = grab(r"Var vs LY.*?kpi-value[^>]*>\+?(-?[\d.]+)%", cast=float)
    gap = grab(r"Gap: \$\+?(-?[\d.]+)M", cast=float)
    cat_neg = grab(r"Categorias en Negativo.*?kpi-value[^>]*>(\d+)", cast=int)
    cat_pos = grab(r"Categorias en Positivo.*?kpi-value[^>]*>(\d+)", cast=int)
    total_cat = grab(r"de (\d+) con datos LY", cast=int)

    return {
        "local": local,
        "corte": corte,
        "fuente": fuente,
        "ventaMtdM": venta_mtd or 0.0,
        "ventaLyM": venta_ly or 0.0,
        "varPct": var_pct or 0.0,
        "gapM": gap or 0.0,
        "catNegativas": cat_neg or 0,
        "catPositivas": cat_pos or 0,
        "totalCategorias": total_cat or 0,
    }


def extract_categorias(html):
    start = html.index("Resumen Completo por Categoria")
    section = html[start:start + 200000]
    end = section.index("</tbody>")
    section = section[:end]

    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", section, re.S)
    data = []
    for r in rows:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        if len(tds) < 6:
            continue
        data.append({
            "categoria": strip_tags(tds[0]),
            "ventaM": to_millions(strip_tags(tds[1])),
            "lyM": to_millions(strip_tags(tds[2])),
            "varPct": to_pct(strip_tags(tds[3])),
            "impactoM": round(to_millions(strip_tags(tds[5])), 2),
        })
    return sorted(data, key=lambda x: x["impactoM"])


def build_bundle(report_path):
    html = Path(report_path).read_text(encoding="utf-8")
    meta = extract_meta(html)
    categorias = extract_categorias(html)
    top_neg = categorias[:3]
    top_pos = list(reversed(categorias[-3:]))
    return {
        "meta": meta,
        "topPositivas": top_pos,
        "topNegativas": top_neg,
        "categorias": categorias,
    }


def render_js_block(bundle):
    data_js = json.dumps(bundle, ensure_ascii=False, indent=4)
    return f"""{BLOCK_START}
        // Datos horneados desde el reporte fuente (snapshot MTD). Para actualizar
        // a un nuevo mes/corte, correr build_septiembre_tab.py de nuevo con el
        // nuevo export.
        const SEPTIEMBRE_DATA = {data_js};

        function renderSeptiembreCategorias() {{
            const meta = SEPTIEMBRE_DATA.meta;
            document.getElementById('sept-subtitle').innerText =
                `Local: ${{meta.local}} - Fuente: ${{meta.fuente}}`;
            document.getElementById('sept-warn').innerText =
                `Corte ${{meta.corte}}. Esto es venta MTD (mes a la fecha), no el mes cerrado.`;

            document.getElementById('sept-kpi-venta').innerText = `$${{meta.ventaMtdM.toFixed(1)}}M`;
            document.getElementById('sept-kpi-venta-sub').innerText = `LY: $${{meta.ventaLyM.toFixed(1)}}M`;

            const varEl = document.getElementById('sept-kpi-var');
            varEl.innerText = `${{meta.varPct >= 0 ? '+' : ''}}${{meta.varPct.toFixed(1)}}%`;
            varEl.style.color = meta.varPct >= 0 ? '#2E7D32' : '#D32F2F';
            document.getElementById('sept-kpi-var-sub').innerText =
                `Gap: $${{meta.gapM >= 0 ? '+' : ''}}${{meta.gapM.toFixed(2)}}M`;

            document.getElementById('sept-kpi-neg').innerText = meta.catNegativas;
            document.getElementById('sept-kpi-neg-sub').innerText = `de ${{meta.totalCategorias}} con datos LY`;
            document.getElementById('sept-kpi-pos').innerText = meta.catPositivas;
            document.getElementById('sept-kpi-pos-sub').innerText = `de ${{meta.totalCategorias}} con datos LY`;

            const posList = document.getElementById('sept-top-pos-list');
            const negList = document.getElementById('sept-top-neg-list');
            posList.innerHTML = '';
            negList.innerHTML = '';

            SEPTIEMBRE_DATA.topPositivas.forEach(item => {{
                const el = document.createElement('div');
                el.className = 'analysis-item';
                el.innerHTML = `
                    <span class="analysis-name" title="${{escapeHtml(item.categoria)}}">${{escapeHtml(item.categoria)}}</span>
                    <span class="trend-badge trend-up">+$${{item.impactoM.toFixed(2)}}M (${{item.varPct >= 0 ? '+' : ''}}${{item.varPct.toFixed(1)}}%)</span>
                `;
                posList.appendChild(el);
            }});

            SEPTIEMBRE_DATA.topNegativas.forEach(item => {{
                const el = document.createElement('div');
                el.className = 'analysis-item';
                el.innerHTML = `
                    <span class="analysis-name" title="${{escapeHtml(item.categoria)}}">${{escapeHtml(item.categoria)}}</span>
                    <span class="trend-badge trend-down">$${{item.impactoM.toFixed(2)}}M (${{item.varPct.toFixed(1)}}%)</span>
                `;
                negList.appendChild(el);
            }});

            // Tabla completa (todas las categorias visibles), resaltando el Top 3 / Bottom 3
            const topPosNames = new Set(SEPTIEMBRE_DATA.topPositivas.map(i => i.categoria));
            const topNegNames = new Set(SEPTIEMBRE_DATA.topNegativas.map(i => i.categoria));

            const tbody = document.getElementById('sept-table-body');
            tbody.innerHTML = SEPTIEMBRE_DATA.categorias.map(item => {{
                let rowBg = '';
                if (topPosNames.has(item.categoria)) rowBg = 'background:rgba(76,175,80,0.10);';
                else if (topNegNames.has(item.categoria)) rowBg = 'background:rgba(229,115,115,0.12);';
                const varColor = item.varPct >= 0 ? '#2E7D32' : '#D32F2F';
                const impColor = item.impactoM >= 0 ? '#2E7D32' : '#D32F2F';
                return `
                    <tr style="border-bottom:1px solid #f0f0f0;${{rowBg}}">
                        <td style="padding:8px 12px;font-weight:600;">${{escapeHtml(item.categoria)}}</td>
                        <td style="padding:8px 12px;text-align:right;">$${{item.ventaM.toFixed(2)}}M</td>
                        <td style="padding:8px 12px;text-align:right;color:#888;">$${{item.lyM.toFixed(2)}}M</td>
                        <td style="padding:8px 12px;text-align:right;font-weight:700;color:${{varColor}};">${{item.varPct >= 0 ? '+' : ''}}${{item.varPct.toFixed(1)}}%</td>
                        <td style="padding:8px 12px;text-align:right;font-weight:700;color:${{impColor}};">${{item.impactoM >= 0 ? '+' : ''}}$${{item.impactoM.toFixed(2)}}M</td>
                    </tr>
                `;
            }}).join('');
        }}
"""


def patch_index(js_block):
    html = INDEX_PATH.read_text(encoding="utf-8")

    if BLOCK_START in html:
        # Ya existe una version anterior: reemplazarla completa (idempotente)
        start = html.index(BLOCK_START)
        end = html.index(BLOCK_END_MARKER, start)
        html = html[:start] + js_block + "\n" + html[end + 1:]
    else:
        # Primera vez: insertar antes de populateSalesFilters
        assert ANCHOR_FALLBACK in html, "No se encontro el punto de insercion esperado"
        html = html.replace(ANCHOR_FALLBACK, ANCHOR_FALLBACK + js_block + "\n", 1)

    INDEX_PATH.write_text(html, encoding="utf-8")


def main():
    report_path = sys.argv[1] if len(sys.argv) > 1 else REPORT_PATH_DEFAULT
    bundle = build_bundle(report_path)
    js_block = render_js_block(bundle)
    patch_index(js_block)
    print(f"OK: pestana Categorias Sept regenerada con {len(bundle['categorias'])} categorias.")
    print(f"Top 3 positivos: {[c['categoria'] for c in bundle['topPositivas']]}")
    print(f"Top 3 negativos: {[c['categoria'] for c in bundle['topNegativas']]}")


if __name__ == "__main__":
    main()
