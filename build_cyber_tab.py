"""
build_cyber_tab.py
-------------------
Genera/actualiza la pestana "Cyber" (checklist operativo de la campana
"Barato a un Click") dentro de index.html.

Los datos de CYBER_DATA salen del webinar operativo (17 paginas, extraido
con pypdf). Si llega una campana nueva (otro Cyber, otras fechas/metas),
editar el diccionario CYBER_DATA de abajo y volver a correr este script.

Uso:
    python build_cyber_tab.py
"""

import json
from pathlib import Path

INDEX_PATH = Path(__file__).parent / "index.html"

BLOCK_START = "        // ---- Checklist Operativo Cyber (Barato a un Click) ----"
BLOCK_END_MARKER = "\n        function populateSalesFilters() {"

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
    "checklist": [
        {
            "seccion": "Reglas de Oro Generales",
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
            "seccion": "Turno Noche (22:00 - 06:30)",
            "items": [
                "21:00 - Trabajar itemes futuros",
                "22:00-22:15 - Reunion de planificacion y entrega de herramientas",
                "22:15-23:00 - Clasificacion de mercaderia / armado de carros",
                "23:00-04:30 - Reposicion 4x1",
                "Ajustes de categorias Top Venta + reposicion estricta de los Nunca Sin",
                "Doble check en Torre de Control: pedidos PU V09:00 del dia siguiente armados",
                "Carga de relojes PU y congelado de Gel Packs",
                "04:30-05:30 - Verificar itemes futuros, identificar quiebres con RF, bajar del bin",
                "05:30-06:00 - Bineo de excedentes (protocolo Espejeo de Bins)",
                "06:00-06:30 - Orden y retiro de cartones",
            ],
        },
        {
            "seccion": "Turno AM (06:30 - 14:00)",
            "items": [
                "Asignacion fija de personal en digital AM",
                "Checklist basico: Reloj, Botonera, Torre, Gel Packs",
                "Asignar armado de pedidos V9, V11 y V13",
                "Revision de la Torre cada 1 hora",
                "Revision de completitud en BI y gestion de quiebres",
                "12:00 hrs (antes de almuerzo): trabajar itemes futuros",
            ],
        },
        {
            "seccion": "Turno PM (14:00 - 22:00)",
            "items": [
                "Asignacion fija de personal en digital PM",
                "Checklist basico: Reloj, Botonera, Torre, Gel Packs",
                "Asignar armado de pedidos V15, V17 y V19",
                "Reposicion en sala segun demanda",
                "Revision de la Torre cada 1 hora y de completitud en BI",
                "17:00-21:00 (Regla de Oro): 1 persona DEDICADA EXCLUSIVAMENTE a entregar "
                "pedidos Pick-Up (60% de las entregas PU ocurren en este bloque)",
            ],
        },
        {
            "seccion": "Rutina Alertas NSG",
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
            "seccion": "Reunion de Planificacion (diaria)",
            "items": [
                "Revisar dotacion vs planificacion (Calculadora)",
                "Asignacion alertas NSG (Mi Repo) 13:00 a 17:00",
                "Asignacion itemes futuros 08:00 a 20:00",
                "Asignacion horneo de pan y pollo",
                "Asignacion zona de pago",
                "Caminata sala de ventas: revisar reposicion de itemes top venta de la campana",
                "Caminata sala de ventas: revisar quiebres visibles",
            ],
        },
        {
            "seccion": "Rutina Gerente de Tienda",
            "items": [
                "07:00-21:00 - Recepcion de camiones",
                "21:00-22:00 (previo a turno noche) - Posicionamiento de pallets en sala de venta",
                "21:00-22:00 - Gestion de devoluciones",
            ],
        },
        {
            "seccion": "Metas / KPI a monitorear a diario",
            "items": [
                "Nuevo NSG >= 96%",
                "Completitud >= 96%",
                "Pallets por persona >= 4",
                "Pickup - Armado a tiempo > 96%",
                "Pickup - Completitud SS > 97% / Completitud CS > 98%",
                "Pickup - TEP < 5 minutos / % Promesa > 85%",
                "Home Delivery - Armado a tiempo > 96%",
                "Home Delivery - Completitud SS > 97% / Completitud CS > 98%",
                "Home Delivery - OTEA > 96% / Same Day > 90% / N2H > 80%",
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
                sec.items.forEach((item, ii) => {{
                    total++;
                    if (state[`${{si}}-${{ii}}`]) done++;
                }});
            }});
            const pct = total ? Math.round((done / total) * 100) : 0;
            document.getElementById('cyber-progress-text').innerText =
                `${{done}} / ${{total}} tareas completadas (${{pct}}%)`;
            document.getElementById('cyber-progress-bar').style.width = `${{pct}}%`;

            document.querySelectorAll('#cyber-checklist-body input[type="checkbox"]').forEach(cb => {{
                const key = cb.dataset.key;
                cb.checked = !!state[key];
                const span = cb.closest('label')?.querySelector('span');
                if (span) {{
                    span.style.textDecoration = cb.checked ? 'line-through' : 'none';
                    span.style.color = cb.checked ? '#9CA3AF' : 'inherit';
                }}
            }});
        }}

        function renderCyberChecklist() {{
            const meta = CYBER_DATA.meta;
            document.getElementById('cyber-subtitle').innerText =
                `${{meta.nombre}} - Del ${{meta.fechaInicio}} al ${{meta.fechaFin}}`;

            document.getElementById('cyber-kpi-venta').innerText = `$${{meta.metaVentaMM.toLocaleString('es-CL')}}M`;
            document.getElementById('cyber-kpi-venta-sub').innerText = `+${{meta.metaVentaVarPct}}% vs LY`;
            document.getElementById('cyber-kpi-pedidos').innerText = meta.metaPedidos.toLocaleString('es-CL');
            document.getElementById('cyber-kpi-pedidos-sub').innerText = `+${{meta.metaPedidosVarPct}}% vs LY`;
            document.getElementById('cyber-kpi-dotacion').innerText = meta.dotacionW40.toLocaleString('es-CL');

            document.getElementById('cyber-foco-body').innerHTML = CYBER_DATA.categoriasFoco.map(c => `
                <tr style="border-bottom:1px solid #f0f0f0;">
                    <td style="padding:6px 10px;"><span style="background:#e8f0fe;color:#0053e2;padding:2px 8px;border-radius:12px;font-size:0.7rem;font-weight:700;">${{escapeHtml(c.tribu)}}</span></td>
                    <td style="padding:6px 10px;font-weight:600;">${{escapeHtml(c.categoria)}}</td>
                    <td style="padding:6px 10px;color:#2a8703;font-weight:700;text-align:right;">${{escapeHtml(c.descuento || '-')}}</td>
                </tr>
            `).join('');

            document.getElementById('cyber-checklist-body').innerHTML = CYBER_DATA.checklist.map((sec, si) => `
                <div class="card shadow-sm" style="padding:1.25rem;margin-bottom:1rem;">
                    <h3 style="color:var(--walmart-blue);margin-bottom:0.75rem;font-size:1rem;">${{escapeHtml(sec.seccion)}}</h3>
                    ${{sec.items.map((item, ii) => `
                        <label style="display:flex;align-items:flex-start;gap:0.6rem;padding:6px 0;border-bottom:1px solid #f5f5f5;cursor:pointer;">
                            <input type="checkbox" data-key="${{si}}-${{ii}}" onchange="toggleCyberItem('${{si}}-${{ii}}')" style="margin-top:3px;flex-shrink:0;">
                            <span style="font-size:0.9rem;">${{escapeHtml(item)}}</span>
                        </label>
                    `).join('')}}
                </div>
            `).join('');

            updateCyberProgress();
        }}
"""


def patch_index(js_block):
    html = INDEX_PATH.read_text(encoding="utf-8")

    if BLOCK_START in html:
        start = html.index(BLOCK_START)
        end = html.index(BLOCK_END_MARKER, start)
        html = html[:start] + js_block + "\n" + html[end + 1:]
    else:
        assert BLOCK_END_MARKER in html, "No se encontro el punto de insercion esperado"
        html = html.replace(BLOCK_END_MARKER, "\n" + js_block + BLOCK_END_MARKER, 1)

    INDEX_PATH.write_text(html, encoding="utf-8")


def main():
    js_block = render_js_block()
    patch_index(js_block)
    total_items = sum(len(s["items"]) for s in CYBER_DATA["checklist"])
    print(f"OK: pestana Cyber regenerada con {len(CYBER_DATA['checklist'])} secciones "
          f"y {total_items} tareas.")


if __name__ == "__main__":
    main()
