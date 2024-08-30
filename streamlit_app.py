import streamlit as st
import json

def generate_code(app_config):
    code = f"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='{app_config['layout']}')

# Data loading
data = pd.read_csv('{app_config['data_source']}')  # Replace with appropriate data loading method

"""
    for component in app_config['components']:
        if component['type'] == 'Chart':
            code += f"""
# {component['type']} component
chart_type = '{component['chart_type']}'
if chart_type == 'bar':
    fig = px.bar(data, x='{component['x_axis']}', y='{component['y_axis']}')
elif chart_type == 'line':
    fig = px.line(data, x='{component['x_axis']}', y='{component['y_axis']}')
elif chart_type == 'scatter':
    fig = px.scatter(data, x='{component['x_axis']}', y='{component['y_axis']}')
st.plotly_chart(fig)
"""
        elif component['type'] == 'Table':
            code += f"""
# {component['type']} component
st.dataframe(data.head({component['num_rows']}))
"""
        elif component['type'] == 'Text':
            code += f"""
# {component['type']} component
st.write('''{component['content']}''')
"""
    return code

def main():
    st.title("Streamlit App Builder")

    # Initialize session state
    if 'app_config' not in st.session_state:
        st.session_state.app_config = {
            'layout': 'wide',
            'data_source': '',
            'components': []
        }

    # 1. Page Layout Selection
    st.header("1. Page Layout")
    layout = st.selectbox("Choose layout", ["wide", "centered"], key="layout")
    st.session_state.app_config['layout'] = layout

    # 2. Data Source Configuration
    st.header("2. Data Source")
    data_source_type = st.selectbox("Select data source type", ["CSV", "Database", "API"])
    data_source = st.text_input("Enter data source (file path, table name, or API endpoint)")
    st.session_state.app_config['data_source'] = data_source

    # 3. Add Components
    st.header("3. Add Components")
    component_type = st.selectbox("Select component type", ["Chart", "Table", "Text"])
    if st.button("Add Component"):
        new_component = {'type': component_type, 'id': len(st.session_state.app_config['components'])}
        st.session_state.app_config['components'].append(new_component)

    # 4. Configure Components
    st.header("4. Configure Components")
    for i, component in enumerate(st.session_state.app_config['components']):
        st.subheader(f"Component {i+1}: {component['type']}")
        if component['type'] == 'Chart':
            component['chart_type'] = st.selectbox("Chart type", ["bar", "line", "scatter"], key=f"chart_type_{i}")
            component['x_axis'] = st.text_input("X-axis column", key=f"x_axis_{i}")
            component['y_axis'] = st.text_input("Y-axis column", key=f"y_axis_{i}")
        elif component['type'] == 'Table':
            component['num_rows'] = st.number_input("Number of rows to display", min_value=1, value=5, key=f"num_rows_{i}")
        elif component['type'] == 'Text':
            component['content'] = st.text_area("Enter text content", key=f"content_{i}")

    # 5. Preview and Generate
    st.header("5. Preview and Generate")
    if st.button("Generate Code"):
        generated_code = generate_code(st.session_state.app_config)
        st.code(generated_code, language="python")

    # Export configuration
    if st.button("Export Configuration"):
        st.download_button(
            label="Download Configuration",
            data=json.dumps(st.session_state.app_config, indent=2),
            file_name="app_config.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
