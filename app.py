import uuid
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 🔒 YOUR SECRET PIN (You can use "1234")
SECRET_PIN = "1234"

# Workspace Data Structure: Holds multiple sections dynamically
notes = [
    {
        "id": str(uuid.uuid4()),
        "title": "📌 Welcome Note",
        "content": "This is your brand new workspace! Click the add button below to build sections, or edit this title.",
        "link": "https://www.google.com"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Smart Workspace</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --card-display-bg: #f8fafc;
            --border-color: #e2e8f0;
            --input-border: #cbd5e1;
            --input-bg: #ffffff;
            --btn-bg: #4f46e5;
            --btn-hover: #4338ca;
            --shadow: rgba(0, 0, 0, 0.04);
        }

        body.dark {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --card-display-bg: #0f172a;
            --border-color: #334155;
            --input-border: #475569;
            --input-bg: #1e293b;
            --btn-bg: #6366f1;
            --btn-hover: #4f46e5;
            --shadow: rgba(0, 0, 0, 0.4);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; transition: background 0.25s ease, color 0.25s ease; }

        body { background: var(--bg-gradient); min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; padding: 40px 20px; }

        .container { background: var(--card-bg); width: 100%; max-width: 600px; border-radius: 24px; box-shadow: 0 12px 40px var(--shadow); padding: 32px; border: 1px solid var(--border-color); }

        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; }
        .header h2 { font-size: 24px; color: var(--text-primary); font-weight: 700; }
        
        .theme-toggle-btn { background: var(--card-display-bg); border: 1px solid var(--border-color); color: var(--text-primary); padding: 8px 14px; border-radius: 12px; cursor: pointer; font-size: 13px; font-weight: 600; }

        .display-card { background: var(--card-display-bg); border: 1px solid var(--border-color); border-radius: 16px; padding: 24px; margin-bottom: 20px; position: relative; }
        
        .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
        .card-title { font-size: 18px; font-weight: 700; color: var(--text-primary); }
        
        .action-btns button { background: none; border: none; font-size: 16px; cursor: pointer; margin-left: 10px; opacity: 0.6; transition: 0.2s; }
        .action-btns button:hover { opacity: 1; transform: scale(1.1); }

        .saved-text { font-size: 15px; color: var(--text-primary); line-height: 1.6; margin-bottom: 14px; white-space: pre-wrap; }
        .saved-link { font-size: 14px; color: var(--btn-bg); text-decoration: none; font-weight: 500; word-break: break-all; }
        .saved-link:hover { text-decoration: underline; }

        .input-group { margin-bottom: 12px; }
        input[type="text"], input[type="password"], textarea { width: 100%; background: var(--input-bg); border: 1px solid var(--input-border); border-radius: 10px; padding: 12px; font-size: 14px; color: var(--text-primary); outline: none; }
        textarea { min-height: 80px; resize: vertical; }
        input:focus, textarea:focus { border-color: var(--btn-bg); }

        .btn-submit { width: 100%; background: var(--btn-bg); color: #ffffff; border: none; border-radius: 10px; padding: 12px; font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 8px; }
        .btn-submit:hover { background: var(--btn-hover); }
        .btn-cancel { width: 100%; background: transparent; color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 10px; padding: 12px; font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 8px; }

        .add-section-btn { width: 100%; background: var(--card-display-bg); border: 2px dashed var(--border-color); color: var(--text-primary); padding: 16px; border-radius: 16px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 8px; transition: 0.2s; }
        .add-section-btn:hover { border-color: var(--btn-bg); color: var(--btn-bg); }

        .alert { padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 500; margin-bottom: 20px; text-align: center; }
        .alert-error { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
        .alert-success { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <h2>🌐 My Smart Workspace</h2>
            <button class="theme-toggle-btn" id="themeToggle" type="button">🌙 Dark Mode</button>
        </div>

        {% if error %}<div class="alert alert-error">{{ error }}</div>{% endif %}
        {% if success %}<div class="alert alert-success">{{ success }}</div>{% endif %}

        {% for note in notes %}
        <div class="display-card">
            
            <div id="view-{{ note.id }}">
                <div class="card-header">
                    <div class="card-title">{{ note.title }}</div>
                    <div class="action-btns">
                        <button onclick="toggleEdit('{{ note.id }}')" title="Edit Heading">✏️</button>
                        <form action="/action" method="POST" style="display:inline;">
                            <input type="hidden" name="action_type" value="delete">
                            <input type="hidden" name="note_id" value="{{ note.id }}">
                            <button type="button" onclick="let pin = prompt('Enter PIN to delete this section:'); if(pin) { this.nextElementSibling.value = pin; this.parentElement.submit(); }" title="Delete Layout">🗑️</button>
                            <input type="hidden" name="pin_data" value="">
                        </form>
                    </div>
                </div>
                <div class="saved-text">{{ note.content }}</div>
                {% if note.link %}<a href="{{ note.link }}" target="_blank" class="saved-link">🔗 {{ note.link }}</a>{% endif %}
            </div>

            <div id="edit-{{ note.id }}" style="display: none;">
                <form action="/action" method="POST">
                    <input type="hidden" name="action_type" value="edit">
                    <input type="hidden" name="note_id" value="{{ note.id }}">
                    
                    <div class="input-group"><input type="text" name="title" value="{{ note.title }}" required></div>
                    <div class="input-group"><textarea name="content">{{ note.content }}</textarea></div>
                    <div class="input-group"><input type="text" name="link" value="{{ note.link }}"></div>
                    <div class="input-group"><input type="password" name="pin_data" placeholder="🔑 Enter PIN to Save Edits" required></div>
                    
                    <button type="submit" class="btn-submit">Save Changes</button>
                    <button type="button" class="btn-cancel" onclick="toggleEdit('{{ note.id }}')">Cancel</button>
                </form>
            </div>
            
        </div>
        {% endfor %}

        <button class="add-section-btn" id="addBtn" onclick="document.getElementById('addFormContainer').style.display='block'; this.style.display='none';">
            ➕ Add New Section
        </button>

        <div id="addFormContainer" class="display-card" style="display: none;">
            <div class="card-title" style="margin-bottom: 15px;">Create New Section</div>
            <form action="/action" method="POST">
                <input type="hidden" name="action_type" value="add">
                <div class="input-group"><input type="text" name="title" placeholder="Heading / Section Name" required></div>
                <div class="input-group"><textarea name="content" placeholder="Type your data or sub-section details here..."></textarea></div>
                <div class="input-group"><input type="text" name="link" placeholder="Paste web link here (optional)..."></div>
                <div class="input-group"><input type="password" name="pin_data" placeholder="🔑 Enter PIN to Add" required></div>
                
                <button type="submit" class="btn-submit">Add to Dashboard</button>
                <button type="button" class="btn-cancel" onclick="document.getElementById('addFormContainer').style.display='none'; document.getElementById('addBtn').style.display='flex';">Cancel</button>
            </form>
        </div>

    </div>

    <script>
        // Theme config
        const themeToggleBtn = document.getElementById('themeToggle');
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark');
            themeToggleBtn.innerHTML = '☀️ Light Mode';
        }
        themeToggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark');
            if (document.body.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.innerHTML = '☀️ Light Mode';
            } else {
                localStorage.setItem('theme', 'light');
                themeToggleBtn.innerHTML = '🌙 Dark Mode';
            }
        });

        function toggleEdit(id) {
            const viewDiv = document.getElementById('view-' + id);
            const editDiv = document.getElementById('edit-' + id);
            if (viewDiv.style.display === 'none') {
                viewDiv.style.display = 'block';
                editDiv.style.display = 'none';
            } else {
                viewDiv.style.display = 'none';
                editDiv.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, notes=notes, error="", success="")

@app.route('/action', methods=['POST'])
def handle_action():
    global notes
    pin = request.form.get('pin_data')
    
    if pin != SECRET_PIN:
        return render_template_string(HTML_TEMPLATE, notes=notes, error="❌ Incorrect PIN! Action denied.", success="")

    action = request.form.get('action_type')

    if action == 'add':
        new_note = {
            "id": str(uuid.uuid4()),
            "title": request.form.get('title', 'Untitled Section'),
            "content": request.form.get('content', ''),
            "link": request.form.get('link', '')
        }
        notes.append(new_note)
        return render_template_string(HTML_TEMPLATE, notes=notes, success="✨ New section added successfully!")

    elif action == 'edit':
        note_id = request.form.get('note_id')
        for note in notes:
            if note['id'] == note_id:
                note['title'] = request.form.get('title')
                note['content'] = request.form.get('content')
                note['link'] = request.form.get('link')
        return render_template_string(HTML_TEMPLATE, notes=notes, success="✨ Section updated!")

    elif action == 'delete':
        note_id = request.form.get('note_id')
        notes = [n for n in notes if n['id'] != note_id]
        return render_template_string(HTML_TEMPLATE, notes=notes, success="🗑️ Section deleted!")

    return render_template_string(HTML_TEMPLATE, notes=notes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
