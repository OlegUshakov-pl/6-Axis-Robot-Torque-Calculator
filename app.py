import math
import streamlit as st

st.set_page_config(page_title="6-Axis Robot Torque Calculator", layout="wide")

st.title("6-Axis Robot Torque Calculator")
st.caption("Static gravity torque calculation and motor/gearbox selection")

GRAVITY = 9.81
SAFETY_FACTOR = 2.0

MOTOR_OPTIONS = [
    {"name": "Motor A", "continuous_nm": 1.5, "peak_nm": 3.0, "rpm": 3000},
    {"name": "Motor B", "continuous_nm": 3.0, "peak_nm": 6.0, "rpm": 3000},
    {"name": "Motor C", "continuous_nm": 5.0, "peak_nm": 10.0, "rpm": 2000},
]

GEARBOX_OPTIONS = [
    {"name": "Gear 10:1", "ratio": 10.0, "efficiency": 0.90},
    {"name": "Gear 20:1", "ratio": 20.0, "efficiency": 0.85},
    {"name": "Gear 50:1", "ratio": 50.0, "efficiency": 0.80},
]

DEFAULT_LINKS = [
    {"name": "J1", "length": 0.30, "mass": 1.2, "com": 0.15},
    {"name": "J2", "length": 0.40, "mass": 1.8, "com": 0.20},
    {"name": "J3", "length": 0.30, "mass": 1.0, "com": 0.15},
    {"name": "J4", "length": 0.20, "mass": 0.7, "com": 0.10},
    {"name": "J5", "length": 0.15, "mass": 0.5, "com": 0.075},
    {"name": "J6", "length": 0.10, "mass": 0.3, "com": 0.05},
]


def gravity_torque(links, payload_mass, angles_deg):
    n = len(links)
    if len(angles_deg) != n:
        return [0.0] * n
    torques = [0.0] * n
    for j in range(n):
        for i in range(j, n):
            arm = 0.0
            cumulative = 0.0
            for k in range(j, i + 1):
                cumulative += angles_deg[k]
                segment = links[k]["com"] if k == i else links[k]["length"]
                arm += segment * math.cos(math.radians(cumulative))
            torques[j] += links[i]["mass"] * GRAVITY * arm
        payload_arm = 0.0
        cumulative = 0.0
        for k in range(j, n):
            cumulative += angles_deg[k]
            payload_arm += links[k]["length"] * math.cos(math.radians(cumulative))
        torques[j] += payload_mass * GRAVITY * payload_arm
    return torques


def select_motor_and_gearbox(required_output_nm):
    candidates = []
    for gearbox in GEARBOX_OPTIONS:
        for motor in MOTOR_OPTIONS:
            output = motor["continuous_nm"] * gearbox["ratio"] * gearbox["efficiency"]
            if output >= required_output_nm:
                candidates.append((output, motor, gearbox))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    output, motor, gearbox = candidates[0]
    return {"motor": motor, "gearbox": gearbox, "available_output_nm": output}


col_sidebar, col_main = st.columns([1, 4])

with col_sidebar:
    st.header("Robot Parameters")

    num_axes = st.number_input("Number of axes", min_value=1, max_value=6, value=6, step=1)

    links = []
    for i in range(num_axes):
        st.subheader(f"Link {i + 1}")
        length = st.number_input(
            f"L{i + 1} length (m)", min_value=0.01, max_value=2.0,
            value=DEFAULT_LINKS[i]["length"] if i < len(DEFAULT_LINKS) else 0.20,
            step=0.01, format="%.2f", key=f"len_{i}"
        )
        mass = st.number_input(
            f"M{i + 1} mass (kg)", min_value=0.01, max_value=50.0,
            value=DEFAULT_LINKS[i]["mass"] if i < len(DEFAULT_LINKS) else 1.0,
            step=0.01, format="%.2f", key=f"mass_{i}"
        )
        com = st.number_input(
            f"COM{i + 1} (m)", min_value=0.01, max_value=2.0,
            value=DEFAULT_LINKS[i]["com"] if i < len(DEFAULT_LINKS) else 0.10,
            step=0.01, format="%.3f", key=f"com_{i}"
        )
        links.append({"name": f"J{i + 1}", "length": length, "mass": mass, "com": com})

# Joint angles need default values before main view renders,
# actual sliders are shown under the torque table in 2 rows.
angles = [
    st.session_state.get(
        f"angle_{i}",
        DEFAULT_LINKS[i].get("angle", 0) if i < len(DEFAULT_LINKS) else 0,
    )
    for i in range(num_axes)
]
payload_mass = st.session_state.get("payload_mass", 5.0)
safety_factor = st.session_state.get("safety_factor", SAFETY_FACTOR)

with col_main:
    col_draw, col_metrics = st.columns([3, 1])

    with col_metrics:
        st.subheader("Results")
        total_mass = sum(link["mass"] for link in links) + payload_mass
        st.metric("Total mass", f"{total_mass:.2f} kg")

        torques = gravity_torque(links, payload_mass, angles)
        for i, torque in enumerate(torques):
            design = abs(torque) * safety_factor
            choice = select_motor_and_gearbox(design)
            if choice:
                pair = f'{choice["motor"]["name"]} + {choice["gearbox"]["name"]}'
            else:
                pair = "No candidate"
            st.metric(f"J{i + 1} torque", f"{torques[i]:.2f} Nm")
            st.caption(f"Design: {design:.2f} Nm | {pair}")

    with col_draw:
        svg_w = 800
        svg_h = 500
        padding = 60

        total_length = sum(link["length"] for link in links) + 0.15
        max_reach = max(total_length, 0.5)

        scale = (svg_w - padding * 2) / max_reach
        base_x = padding + 30
        base_y = svg_h - padding

        svg_lines = []

        svg_lines.append(
            f'<line x1="{padding}" y1="{base_y}" x2="{svg_w - padding}" y2="{base_y}" '
            f'stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,5" />'
        )

        svg_lines.append(
            f'<rect x="{base_x - 15}" y="{base_y}" width="30" height="20" '
            f'fill="#64748b" stroke="#334155" stroke-width="2" rx="3" />'
        )

        cumulative_angle = 0.0
        x_prev = base_x
        y_prev = base_y

        link_positions = []

        for i, link in enumerate(links):
            cumulative_angle += angles[i]
            x_end = x_prev + link["length"] * scale * math.cos(math.radians(cumulative_angle))
            y_end = y_prev - link["length"] * scale * math.sin(math.radians(cumulative_angle))

            link_positions.append({
                "x_start": x_prev, "y_start": y_prev,
                "x_end": x_end, "y_end": y_end,
                "length": link["length"], "mass": link["mass"]
            })

            svg_lines.append(
                f'<line x1="{x_prev}" y1="{y_prev}" x2="{x_end}" y2="{y_end}" '
                f'stroke="#3b82f6" stroke-width="6" stroke-linecap="round" />'
            )

            svg_lines.append(
                f'<circle cx="{x_end}" cy="{y_end}" r="5" '
                f'fill="#f97316" stroke="#1e293b" stroke-width="1.5" />'
            )

            svg_lines.append(
                f'<circle cx="{x_prev}" cy="{y_prev}" r="4" '
                f'fill="#1e293b" stroke="#64748b" stroke-width="1" />'
            )

            x_prev = x_end
            y_prev = y_end

        payload_r = max(6, 3 + payload_mass * 0.5)
        svg_lines.append(
            f'<circle cx="{x_end}" cy="{y_end}" r="{payload_r}" '
            f'fill="#ef4444" stroke="#1e293b" stroke-width="1.5" />'
        )
        svg_lines.append(
            f'<text x="{x_end + 8}" y="{y_end - 8}" fill="#ef4444" '
            f'font-family="sans-serif" font-size="11" font-weight="bold">'
            f'{payload_mass:.1f} kg</text>'
        )

        for i, pos in enumerate(link_positions):
            mx = (pos["x_start"] + pos["x_end"]) / 2
            my = (pos["y_start"] + pos["y_end"]) / 2
            svg_lines.append(
                f'<text x="{mx - 5}" y="{my - 10}" fill="#1e293b" '
                f'font-family="sans-serif" font-size="10" font-weight="bold">'
                f'J{i + 1}</text>'
            )

            dx = pos["x_end"] - pos["x_start"]
            dy = pos["y_end"] - pos["y_start"]
            length_px = math.sqrt(dx ** 2 + dy ** 2)
            if length_px > 30:
                nx = -dy / length_px
                ny = dx / length_px
                offset = 15
                lx = mx + nx * offset
                ly = my + ny * offset
                svg_lines.append(
                    f'<text x="{lx}" y="{ly}" fill="#64748b" '
                    f'font-family="sans-serif" font-size="10" text-anchor="middle">'
                    f'{pos["length"]:.2f} m</text>'
                )

        svg_content = "\n".join(svg_lines)
        svg_wrapper = f"""
        <svg width="{svg_w}" height="{svg_h}" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
            <defs>
                <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="1"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            {svg_content}
        </svg>
        """

        st.subheader("Robot Arm View")
        st.components.v1.html(svg_wrapper, height=svg_h + 20)

    st.subheader("Joint Angles (deg)")
    # Two rows, compact sliders, right under the figure.
    half = (num_axes + 1) // 2
    new_angles = []
    for row in (range(half), range(half, num_axes)):
        cols = st.columns(len(row))
        for col, i in zip(cols, row):
            with col:
                angle = st.slider(
                    f"J{i + 1} angle", min_value=-180, max_value=180,
                    value=int(st.session_state.get(
                        f"angle_{i}",
                        DEFAULT_LINKS[i].get("angle", 0) if i < len(DEFAULT_LINKS) else 0,
                    )),
                    step=1, key=f"angle_{i}",
                )
                new_angles.append((i, angle))
    new_angles = [a for _, a in sorted(new_angles)]

    st.markdown("---")
    st.subheader("Torque Table")

    table_data = []
    for i, torque in enumerate(torques):
        design = abs(torque) * safety_factor
        choice = select_motor_and_gearbox(design)
        if choice:
            pair = f'{choice["motor"]["name"]} + {choice["gearbox"]["name"]}'
            available = f'{choice["available_output_nm"]:.2f} Nm'
        else:
            pair = "No candidate"
            available = "—"
        table_data.append({
            "Joint": f"J{i + 1}",
            "Gravity Torque (Nm)": f"{torque:.2f}",
            "Design Torque (Nm)": f"{design:.2f}",
            "Motor + Gearbox": pair,
            "Available Output": available,
        })

    st.dataframe(table_data, use_container_width=True)

    st.markdown("---")
    col_payload, col_safety = st.columns(2)
    with col_payload:
        st.subheader("Payload")
        st.number_input(
            "Payload mass (kg)", min_value=0.0, max_value=100.0,
            value=float(payload_mass), step=0.1, format="%.1f",
            key="payload_mass",
        )
    with col_safety:
        st.subheader("Safety")
        st.number_input(
            "Safety factor", min_value=1.0, max_value=5.0,
            value=float(safety_factor), step=0.1, format="%.1f",
            key="safety_factor",
        )

st.markdown("---")
st.caption("Version: 3.0 | Static gravity torque model (first approximation)")
