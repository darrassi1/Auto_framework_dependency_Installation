
from nbconvert import HTMLExporter
import papermill as pm

import nbformat as nbf


def process_notebook(project_dir, project_name, notebook_path, user_input, output_path):
    try:
        # Ensure project directory exists
        if not os.path.exists(project_dir):
            os.makedirs(project_dir, exist_ok=True)

        construct_path = os.path.join(project_dir, project_name, notebook_path)
        logging.info(f"Construct path: {construct_path}")
        output_path1 = os.path.join(project_dir, project_name, output_path)
        logging.info(f"Output path: {output_path1}")

        # Load or create notebook
        if not os.path.exists(construct_path):
            nb = nbf.v4.new_notebook()
            with open(construct_path, 'w', encoding="utf-8") as f:
                nbf.write(nb, f)
        else:
            nb = nbf.read(construct_path, as_version=4)
        logging.info("Notebook loaded or created successfully.")

        # Insert new cell with user input
        new_cell = nbf.v4.new_code_cell(user_input)
        nb.cells.append(new_cell)

        # Save updated notebook
        with open(construct_path, 'w', encoding="utf-8") as f:
            nbf.write(nb, f)
        logging.info("User input cell added and notebook saved.")

        # Execute notebook
        pm.execute_notebook(construct_path, output_path1)
        logging.info("Notebook executed successfully.")

        # Convert executed notebook to HTML
        with open(output_path1, encoding="utf-8") as f:
            executed_nb = nbf.read(f, as_version=4)

        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(executed_nb)
        logging.info("Notebook converted to HTML successfully.")

        return body, resources
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, None


@app.route('/executenotebook', methods=['POST'])
def execute_notebook():
    user_input = request.json.get('input')
    project_name = request.json.get("project_name")
    print(f"Received user input: {user_input}")

    notebook_path = 'template.ipynb'
    output_path = 'output.ipynb'
    # Process the notebook sequentially
    body, resources = process_notebook(project_dir, project_name, notebook_path, user_input, output_path)

    return jsonify({'html': body})
