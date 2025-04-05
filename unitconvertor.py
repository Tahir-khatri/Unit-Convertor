import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    initial_sidebar_state="expanded"
)

def main():
    # Initial CSS for both themes
    st.markdown("""
        <style>
        /* Base styles */
        .settings-title {
            color: #333;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .toggle-container {
            background-color: #f0f0f0;
            border-radius: 25px;
            padding: 5px;
            width: 200px;
            height: 40px;
            position: relative;
            cursor: pointer;
            margin: 10px 0;
        }
        .toggle-container.dark {
            background-color: #333;
        }
        .toggle-text {
            position: absolute;
            left: 50px;
            top: 50%;
            transform: translateY(-50%);
            color: #333;
            font-weight: bold;
        }
        .toggle-container.dark .toggle-text {
            color: white;
        }
        .toggle-circle {
            width: 30px;
            height: 30px;
            background: white;
            border-radius: 50%;
            position: absolute;
            left: 5px;
            top: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Dark theme text colors */
        .dark-mode .stTextInput input,
        .dark-mode .stTextInput textarea,
        .dark-mode .stSelectbox select,
        .dark-mode .stNumberInput input,
        .dark-mode .stSelectbox span,
        .dark-mode .stMarkdown p,
        .dark-mode .stMarkdown span,
        .dark-mode label,
        .dark-mode .stTextInput label,
        .dark-mode .stSelectbox label,
        .dark-mode .stNumberInput label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Theme options in sidebar
    with st.sidebar:
        # Custom settings title with black color
        st.markdown('<h1 style="color: #333;">Settings</h1>', unsafe_allow_html=True)
        
        current_theme = st.session_state.get('theme', 'light')
        
        # Custom HTML for theme toggle
        toggle_html = f"""
        <div class="toggle-container {'dark' if current_theme == 'dark' else ''}"
             onclick="document.querySelector('#{'dark' if current_theme == 'light' else 'light'}_theme_btn').click()">
            <div class="toggle-circle">{'🌙' if current_theme == 'dark' else '☀️'}</div>
            <span class="toggle-text">{'NIGHT MODE' if current_theme == 'dark' else 'DAY MODE'}</span>
        </div>
        """
        st.markdown(toggle_html, unsafe_allow_html=True)
        
        # Hidden buttons for handling clicks
        if st.button("Light Theme", key="light_theme_btn", type="primary"):
            st.session_state.theme = "light"
            st.rerun()
        if st.button("Dark Theme", key="dark_theme_btn", type="primary"):
            st.session_state.theme = "dark"
            st.rerun()

        # Apply dark theme
        if st.session_state.get('theme') == "dark":
            st.markdown("""
                <style>
                    body {
                        color: white !important;
                    }
                    .stApp {
                        background-color: #111;
                        color: white !important;
                    }
                    .stButton button {
                        background-color: #333;
                        color: white !important;
                    }
                    .stSelectbox div[data-baseweb="select"] {
                        background-color: #333;
                        color: white !important;
                    }
                    .stNumberInput div[data-baseweb="input"] {
                        background-color: #333;
                    }
                    .stNumberInput input {
                        color: black !important;
                        background-color: white !important;
                    }
                    /* Labels and headings in white */
                    .stMarkdown, .stSelectbox,
                    .stMarkdown p, .stMarkdown span,
                    .stSelectbox span,
                    label, .stTextInput label, .stSelectbox label, .stNumberInput label {
                        color: white !important;
                    }
                    /* Ensure dropdown items are white */
                    [data-baseweb="select"] ul li {
                        color: white !important;
                    }
                </style>
                """, unsafe_allow_html=True)
            # Add dark-mode class to body
            st.markdown("""
                <script>
                    document.body.classList.add('dark-mode');
                </script>
                """, unsafe_allow_html=True)

    st.title("Unit Converter")
    st.write("Convert between different units of measurement")

    # Select conversion category
    category = st.selectbox(
        "Select Category",
        ["Length", "Weight", "Temperature", "Time"]
    )

    # Create conversion functions for each category
    def length_conversion(value, from_unit, to_unit):
        # Base unit is meters
        length_units = {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Mile": 1609.34,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254
        }
        # Convert to base unit first
        base_value = value * length_units[from_unit]
        # Convert from base unit to target unit
        return base_value / length_units[to_unit]

    def weight_conversion(value, from_unit, to_unit):
        # Base unit is kilograms
        weight_units = {
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 0.000001,
            "Pound": 0.453592,
            "Ounce": 0.0283495
        }
        base_value = value * weight_units[from_unit]
        return base_value / weight_units[to_unit]

    def temperature_conversion(value, from_unit, to_unit):
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif to_unit == "Kelvin":
                return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32
        return value

    def time_conversion(value, from_unit, to_unit):
        # Base unit is seconds
        time_units = {
            "Second": 1,
            "Minute": 60,
            "Hour": 3600,
            "Day": 86400,
            "Week": 604800
        }
        base_value = value * time_units[from_unit]
        return base_value / time_units[to_unit]

    # Define units for each category
    units = {
        "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
        "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
        "Time": ["Second", "Minute", "Hour", "Day", "Week"]
    }

    # Create input fields
    col1, col2 = st.columns(2)
    
    with col1:
        value = st.number_input("Enter Value", value=0.0)
        from_unit = st.selectbox("From Unit", units[category])

    with col2:
        st.write("")  # Empty space to align with number input
        to_unit = st.selectbox("To Unit", units[category])

    # Perform conversion
    if st.button("Convert"):
        if category == "Length":
            result = length_conversion(value, from_unit, to_unit)
        elif category == "Weight":
            result = weight_conversion(value, from_unit, to_unit)
        elif category == "Temperature":
            result = temperature_conversion(value, from_unit, to_unit)
        else:  # Time
            result = time_conversion(value, from_unit, to_unit)

        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

    # Add some helpful information
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Select the category of conversion (Length, Weight, Temperature, or Time)
    2. Enter the value you want to convert
    3. Select the unit to convert from
    4. Select the unit to convert to
    5. Click the Convert button
    """)

if __name__ == "__main__":
    main()

st.write("Made with ❤️ by [Tahir Khatri](https://github.com/Tahir-Khatri)")