"""
build_cyber_tab.py
-------------------
Genera/actualiza la pestana "Cyber" (checklist operativo de la campana
"Barato a un Click") dentro de index.html.

Version 2: recortada a solo 3 secciones (Reglas de Oro, Rutina Alertas NSG,
Rutina Itemes Futuros) y con un render mas ludico/visual: tarjetas grandes
para las Reglas de Oro, timeline numerada para las rutinas paso a paso,
chips de colores para categorias foco, y una barra de progreso animada con
mensajes segun el avance.

Si llega una campana nueva (otro Cyber, otras fechas/metas), editar el
diccionario CYBER_DATA de abajo y volver a correr este script.

Uso:
    python build_cyber_tab.py
"""

import json
from pathlib import Path

INDEX_PATH = Path(__file__).parent / "index.html"

BLOCK_START = "        // ---- Checklist Operativo Cyber (Barato a un Click) ----"
BLOCK_END_TAG = "        // ---- FIN Checklist Cyber ----\n"
# Ancla estable de fin de <script> (independiente de otras pestanas generadas,
# como Categorias Sept). Se usa solo la primera vez que se inserta el bloque.
ANCHOR_FALLBACK = "\n        init();\n    </script>"

CYBER_DATA = {
    "meta": {
        "nombre": "Barato a un Click",
        "fechaInicio": "28-09-2026",
        "fechaFin": "11-10-2026",
        "metaVentaMM": 3607,
        "metaVentaVarPct": 151,
        "metaPedidos": 76589,
        "metaPedidosVarPct": 98,
        "dotacionW40": 4800,
    },
    "categoriasFoco": [
        {"tribu": "ACP", "categoria": "Panales Bebe", "descuento": "hasta 45% Off"},
        {"tribu": "ACP", "categoria": "Bebidas - Cafe", "descuento": ""},
        {"tribu": "ACP", "categoria": "Papel Higienico", "descuento": ""},
        {"tribu": "PPS", "categoria": "Leche - Crema", "descuento": "desde $880"},
        {"tribu": "PPS", "categoria": "Quesos Autoservicio", "descuento": ""},
        {"tribu": "PPS", "categoria": "Pan - Gondola", "descuento": ""},
        {"tribu": "GM", "categoria": "Menaje Mesa", "descuento": "hasta 45% Off"},
        {"tribu": "GM", "categoria": "Hidratacion y Conservacion", "descuento": ""},
        {"tribu": "GM", "categoria": "Menaje Cocina", "descuento": ""},
    ],
    # Metas de la campana a nivel comercial (pagina 3 del webinar). Se muestran
    # como chips debajo de las categorias foco, es info de contexto, no tareas.
    "metasCampana": [
        {"label": "Market Share W40", "valor": "5.77%"},
        {"label": "Market Share W41", "valor": "4.0%"},
        {"label": "Productos en Campana", "valor": "227"},
        {"label": "Exclusivos SBA", "valor": "12%"},
        {"label": "Price Gap vs LMB", "valor": "8.12%"},
        {"label": "Participacion APP", "valor": "50%"},
    ],
    # Solo las 3 secciones mas importantes, elegidas para que sean las
    # protagonistas del tab (el resto del checklist operativo completo
    # sigue disponible en el webinar fuente, esto es el "top 3" a la vista).
    "checklist": [
        {
            "seccion": "Reglas de Oro Generales",
            "tipo": "reglas",
            "items": [
                "Shoppers: ingreso 7:30 hrs",
                "Botonera / Reloj Operativo cargado 100% desde el inicio de turno",
                "Apoyo activo de encontrabilidad de productos a shoppers (el shopper es un cliente)",
                "Revision de seguridad en salida de Home Delivery",
                "Protocolo paperless listo por si hay contingencia",
                "Torre de Control con alerta/lista visible y actualizada",
                "Gel Packs congelados OK",
            ],
        },
        {
            "seccion": "Rutina Alertas NSG",
            "tipo": "pasos",
            "color": "#0053e2",
            "items": [
                "07:30-12:30 - Imprimir alertas NSG",
                "Ingresar a la aplicacion IMS",
                "Pistolear el codigo de barra del reporte del nuevo NSG",
                "Prioridad 1: gestionar alertas GM",
                "Prioridad 2: gestionar alertas ACP",
                "Prioridad 3: gestionar alertas PPS",
                "NSG WIC: revisar disponibilidad",
                "17:30 - Recepcion y chequeo de alertas gestionadas",
            ],
        },
        {
            "seccion": "Rutina Itemes Futuros",
            "tipo": "pasos",
            "color": "#2E7D32",
            "items": [
                "Imprimir itemes futuros e itemes top quiebre "
                "(horarios: 08:00, 11:00, 13:00, 15:00, 17:00, 19:00)",
                "Entregar los dos reportes a personal asignado",
                "Personal asignado recorre y chequea quiebres del reporte de itemes futuros",
                "Personal asignado repone itemes, prioridad en top quiebres",
                "Priorizar por cantidad de unidades vendidas, trabajar itemes del mismo dia",
                "Entregar reporte a Gerente de Tienda para definir nuevos focos",
            ],
        },
        {
            "seccion": "Metas KPI a Monitorear",
            "tipo": "metas",
            "grupos": [
                {
                    "nombre": "Disponibilidad y Productividad",
                    "items": [
                        {"label": "Nuevo NSG", "meta": ">= 96%"},
                        {"label": "Completitud", "meta": ">= 96%"},
                        {"label": "Pallets por persona", "meta": ">= 4"},
                    ],
                },
                {
                    "nombre": "Pickup",
                    "items": [
                        {"label": "Armado a tiempo", "meta": "> 96%"},
                        {"label": "Completitud SS", "meta": "> 97%"},
                        {"label": "Completitud CS", "meta": "> 98%"},
                        {"label": "TEP (espera cliente)", "meta": "< 5 min"},
                        {"label": "% Promesa", "meta": "> 85%"},
                    ],
                },
                {
                    "nombre": "Home Delivery",
                    "items": [
                        {"label": "Armado a tiempo", "meta": "> 96%"},
                        {"label": "Completitud SS", "meta": "> 97%"},
                        {"label": "Completitud CS", "meta": "> 98%"},
                        {"label": "OTEA", "meta": "> 96%"},
                        {"label": "Same Day", "meta": "> 90%"},
                        {"label": "N2H", "meta": "> 80%"},
                    ],
                },
            ],
        },
    ],
}


def render_js_block():
    data_js = json.dumps(CYBER_DATA, ensure_ascii=False, indent=4)
    return f"""{BLOCK_START}
        // Datos horneados desde el webinar operativo de la campana. Para una
        // nueva campana, editar CYBER_DATA en build_cyber_tab.py y re-correr.
        const CYBER_DATA = {data_js};

        function getCyberChecklistState() {{
            try {{
                return JSON.parse(localStorage.getItem('cyber_checklist_v1')) || {{}};
            }} catch (e) {{
                return {{}};
            }}
        }}

        function setCyberChecklistState(state) {{
            localStorage.setItem('cyber_checklist_v1', JSON.stringify(state));
        }}

        function toggleCyberItem(key) {{
            const state = getCyberChecklistState();
            state[key] = !state[key];
            setCyberChecklistState(state);
            updateCyberProgress();
        }}

        function resetCyberChecklist() {{
            if (!confirm('Reiniciar el checklist de Barato a un Click?')) return;
            localStorage.removeItem('cyber_checklist_v1');
            updateCyberProgress();
        }}

        function updateCyberProgress() {{
            const state = getCyberChecklistState();
            let total = 0, done = 0;
            CYBER_DATA.checklist.forEach((sec, si) => {{
                if (sec.tipo === 'metas') return; // metas informativas, no son tareas checkeables
                sec.items.forEach((item, ii) => {{
                    total++;
                    if (state[`${{si}}-${{ii}}`]) done++;
                }});
            }});
            const pct = total ? Math.round((done / total) * 100) : 0;

            let mensaje = 'Vamos que se puede, arranca marcando la primera tarea';
            if (pct >= 100) mensaje = 'Local listo para el Cyber. Gran trabajo del equipo &#127881;';
            else if (pct >= 70) mensaje = 'Ya casi. Los ultimos detalles hacen la diferencia';
            else if (pct >= 30) mensaje = 'Vas bien encaminado, dale que se puede';

            document.getElementById('cyber-progress-text').innerText = `${{done}} / ${{total}} tareas completadas (${{pct}}%)`;
            document.getElementById('cyber-progress-msg').innerHTML = mensaje;
            document.getElementById('cyber-progress-bar').style.width = `${{pct}}%`;

            document.querySelectorAll('#cyber-checklist-body input.cyber-checkbox').forEach(cb => {{
                const key = cb.dataset.key;
                const isDone = !!state[key];
                cb.checked = isDone;
                const label = cb.closest('label');
                const textSpan = label ? label.querySelector('.cyber-item-text') : null;
                if (textSpan) {{
                    textSpan.style.textDecoration = isDone ? 'line-through' : 'none';
                    textSpan.style.color = isDone ? '#9CA3AF' : 'inherit';
                }}
            }});

            document.querySelectorAll('.cyber-step-badge').forEach(badge => {{
                const key = badge.dataset.badge;
                badge.classList.toggle('done', !!state[key]);
            }});
        }}

        function renderCyberRuleCard(item, si, ii) {{
            return `
                <label class="cyber-rule-card">
                    <input type="checkbox" class="cyber-checkbox" data-key="${{si}}-${{ii}}" onchange="toggleCyberItem('${{si}}-${{ii}}')">
                    <span class="cyber-item-text" style="font-weight:600;line-height:1.4;">${{escapeHtml(item)}}</span>
                </label>
            `;
        }}

        function renderCyberStepItem(item, si, ii, color) {{
            return `
                <label class="cyber-step-item">
                    <span class="cyber-step-badge" style="background:${{color}};" data-badge="${{si}}-${{ii}}">${{ii + 1}}</span>
                    <span style="display:flex;align-items:center;gap:0.6rem;flex:1;padding-top:4px;">
                        <input type="checkbox" class="cyber-checkbox" data-key="${{si}}-${{ii}}" onchange="toggleCyberItem('${{si}}-${{ii}}')">
                        <span class="cyber-item-text">${{escapeHtml(item)}}</span>
                    </span>
                </label>
            `;
        }}

        function renderCyberMetasCard(sec) {{
            return `
                <div class="card shadow-sm" style="padding:1.5rem;margin-bottom:1.5rem;border-top:5px solid #7B1FA2;">
                    <h3 style="font-size:1.15rem;margin-bottom:1rem;color:#7B1FA2;">&#127919; ${{escapeHtml(sec.seccion)}}</h3>
                    ${{sec.grupos.map(g => `
                        <div style="margin-bottom:1rem;">
                            <div style="font-size:0.8rem;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.5rem;">${{escapeHtml(g.nombre)}}</div>
                            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0.6rem;">
                                ${{g.items.map(it => `
                                    <div class="cyber-meta-badge">
                                        <div style="font-size:0.7rem;color:#6A1B9A;font-weight:600;">${{escapeHtml(it.label)}}</div>
                                        <div style="font-size:1.05rem;font-weight:800;color:#4A148C;">${{escapeHtml(it.meta)}}</div>
                                    </div>
                                `).join('')}}
                            </div>
                        </div>
                    `).join('')}}
                </div>
            `;
        }}

        function renderCyberSection(sec, si) {{
            if (sec.tipo === 'reglas') {{
                return `
                    <div class="card shadow-sm" style="padding:1.5rem;margin-bottom:1.5rem;border-top:5px solid var(--walmart-yellow);">
                        <h3 style="font-size:1.15rem;margin-bottom:1rem;color:#7a5200;">&#127942; ${{escapeHtml(sec.seccion)}}</h3>
                        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.85rem;">
                            ${{sec.items.map((item, ii) => renderCyberRuleCard(item, si, ii)).join('')}}
                        </div>
                    </div>
                `;
            }}
            if (sec.tipo === 'metas') {{
                return renderCyberMetasCard(sec);
            }}
            const color = sec.color || 'var(--walmart-blue)';
            const icono = color === '#0053e2' ? '&#128269;' : '&#128230;';
            return `
                <div class="card shadow-sm" style="padding:1.5rem;margin-bottom:1.5rem;border-top:5px solid ${{color}};">
                    <h3 style="font-size:1.15rem;margin-bottom:0.5rem;color:${{color}};">${{icono}} ${{escapeHtml(sec.seccion)}}</h3>
                    <div>
                        ${{sec.items.map((item, ii) => renderCyberStepItem(item, si, ii, color)).join('')}}
                    </div>
                </div>
            `;
        }}

        function renderCyberChecklist() {{
            const meta = CYBER_DATA.meta;
            document.getElementById('cyber-subtitle').innerText =
                `Del ${{meta.fechaInicio}} al ${{meta.fechaFin}}`;

            document.getElementById('cyber-kpi-venta').innerText = `$${{meta.metaVentaMM.toLocaleString('es-CL')}}M`;
            document.getElementById('cyber-kpi-venta-sub').innerText = `+${{meta.metaVentaVarPct}}% vs LY`;
            document.getElementById('cyber-kpi-pedidos').innerText = meta.metaPedidos.toLocaleString('es-CL');
            document.getElementById('cyber-kpi-pedidos-sub').innerText = `+${{meta.metaPedidosVarPct}}% vs LY`;
            document.getElementById('cyber-kpi-dotacion').innerText = meta.dotacionW40.toLocaleString('es-CL');

            const chipBg = {{ ACP: '#E3F2FD', PPS: '#FFF3E0', GM: '#E8F5E9' }};
            const chipText = {{ ACP: '#0053e2', PPS: '#e07000', GM: '#2E7D32' }};
            document.getElementById('cyber-foco-body').innerHTML = CYBER_DATA.categoriasFoco.map(c => `
                <div class="cyber-chip" style="background:${{chipBg[c.tribu] || '#F5F5F5'}};">
                    <span style="font-size:0.65rem;font-weight:800;letter-spacing:0.5px;color:${{chipText[c.tribu] || '#555'}};">${{escapeHtml(c.tribu)}}</span>
                    <span style="font-size:0.85rem;font-weight:700;">${{escapeHtml(c.categoria)}}</span>
                    ${{c.descuento ? `<span style="font-size:0.8rem;font-weight:800;color:#2a8703;">${{escapeHtml(c.descuento)}}</span>` : ''}}
                </div>
            `).join('');

            document.getElementById('cyber-metas-campana-body').innerHTML = CYBER_DATA.metasCampana.map(m => `
                <div class="cyber-meta-badge">
                    <div style="font-size:0.7rem;color:#6A1B9A;font-weight:600;">${{escapeHtml(m.label)}}</div>
                    <div style="font-size:1.05rem;font-weight:800;color:#4A148C;">${{escapeHtml(m.valor)}}</div>
                </div>
            `).join('');

            document.getElementById('cyber-checklist-body').innerHTML =
                CYBER_DATA.checklist.map((sec, si) => renderCyberSection(sec, si)).join('');

            updateCyberProgress();
        }}
{BLOCK_END_TAG}"""


def patch_index(js_block):
    html = INDEX_PATH.read_text(encoding="utf-8")

    if BLOCK_START in html:
        start = html.index(BLOCK_START)
        end = html.index(BLOCK_END_TAG, start) + len(BLOCK_END_TAG)
        html = html[:start] + js_block + html[end:]
    else:
        assert ANCHOR_FALLBACK in html, "No se encontro el punto de insercion esperado"
        html = html.replace(ANCHOR_FALLBACK, "\n" + js_block + ANCHOR_FALLBACK, 1)

    INDEX_PATH.write_text(html, encoding="utf-8")


def main():
    js_block = render_js_block()
    patch_index(js_block)
    total_items = sum(len(s["items"]) for s in CYBER_DATA["checklist"] if s["tipo"] != "metas")
    print(f"OK: pestana Cyber regenerada con {len(CYBER_DATA['checklist'])} secciones "
          f"y {total_items} tareas.")


if __name__ == "__main__":
    main()
