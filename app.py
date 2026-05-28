import uuid
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
# Secure secret key required for handling login sessions safely
app.secret_key = "workspace_front_door_key_77"

# 🔒 YOUR MASTER PASSWORD (Type this once when you open the website)
MASTER_PIN = "1234"

# Workspace Data Storage
notes = [
    {
        "id": str(uuid.uuid4()),
        "title": "Gemini",
        "content": "great work and best help",
        "link": "https://gemini.google.com/"
    }
]

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workspace Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif; padding: 20px; }
        .login-card { background: #1e293b; width: 100%; max-width: 400px; padding: 40px 32px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); border: 1px solid #334155; text-align: center; }
        h2 { color: #f8fafc; font-size: 26px; font-weight: 700; margin-bottom: 8px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
        input[type="password"] { width: 100%; background: #0f172a; border: 1px solid #475569; border-radius: 12px; padding: 14px; font-size: 16px; color: #f8fafc; outline: none; text-align: center; letter-spacing: 4px; transition: 0.2s; margin-bottom: 16px; }
        input[type="password"]:focus { border-color: #6366f1; box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2); }
        .btn-login { width: 100%; background: #6366f1; color: #ffffff; border: none; border-radius: 12px; padding: 14px; font-size: 16px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-login:hover { background: #4f46e5; }
        .alert { background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 500; margin-bottom: 16px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>🔒 Workspace Locked</h2>
        <p>Please enter your master security PIN to open your workspace.</p>
        {% if error %}<div class="alert">{{ error }}</div>{% endif %}
        <form action="/login" method="POST">
            <input type="password" name="pin" placeholder="••••" autocomplete="off" autofocus required>
            <button type="submit" class="btn-login">Unlock Dashboard</button>
        </form>
    </div>
</body>
</html>
"""

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
        
        .header-actions { display: flex; gap: 10px; align-items: center; }
        .theme-toggle-btn, .logout-btn { background: var(--card-display-bg); border: 1px solid var(--border-color); color: var(--text-primary); padding: 8px 14px; border-radius: 12px; cursor: pointer; font-size: 13px; font-weight: 600; text-decoration: none; }
        .logout-btn { background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2); }
        .logout-btn:hover { background: #ef4444; color: #fff; }

        .display-card { background: var(--card-display-bg); border: 1px solid var(--border-color); border-radius: 16px; padding: 24px; margin-bottom: 20px; position: relative; }
        
        .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
        .card-title { font-size: 18px; font-weight: 700; color: var(--text-primary); }
        
        .action-btns button { background: none; border: none; font-size: 16px; cursor: pointer; margin-left: 10px; opacity: 0.6; transition: 0.2s; }
        .action-btns button:hover { opacity: 1; transform: scale(1.1); }

        .saved-text { font-size: 15px; color: var(--text-primary); line-height: 1.6; margin-bottom: 14px; white-space: pre-wrap; }
        .saved-link { font-size: 14px; color: var(--btn-bg); text-decoration: none; font-weight: 500; word-break: break-all; }
        .saved-link:hover { text-decoration: underline; }

        .input-group { margin-bottom: 12px; }
        input[type="text"], textarea { width: 100%; background: var(--input-bg); border: 1px solid var(--input-border); border-radius: 10px; padding: 12px; font-size: 14px; color: var(--text-primary); outline: none; }
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
            <div class="header-actions">
                <button class="theme-toggle-btn" id="themeToggle" type="button">☀️ Light Mode</button>
                <a href="/logout" class="logout-btn">🔒 Lock</a>
            </div>
        </div>

        {% if error %}<div class="alert alert-error">{{ error }}</div>{% endif %}
        {% if success %}<div class="alert alert-success">{{ success }}</div>{% endif %}

        <!-- Loop for existing notes -->
        {% for note in notes %}
        <div class="display-card">
            
            <!-- View Mode -->
            <div id="view-{{ note.id }}">
                <div class="card-header">
                    <div class="card-title">{{ note.title }}</div>
                    <div class="action-btns">
                        <button onclick="toggleEdit('{{ note.id }}')" title="Edit Layout">✏️</button>
                        <form action="/action" method="POST" style="display:inline;">
                            <input type="hidden" name="action_type" value="delete">
                            <input type="hidden" name="note_id" value="{{ note.id }}">
                            <button type="submit" onclick="return confirm('Are you sure you want to delete this section?')" title="Delete Layout">🗑️</button>
                        </form>
                    </div>
                </div>
                <div class="saved-text">{{ note.content }}</div>
                {% if note.link %}<a href="{{ note.link }}" target="_blank" class="saved-link">🔗 {{ note.link }}</a>{% endif %}
            </div>

            <!-- Edit Mode (NO PASSWORD REQUIREMENT HERE) -->
            <div id="edit-{{ note.id }}" style="display: none;">
                <form action="/action" method="POST">
                    <input type="hidden" name="action_type" value="edit">
                    <input type="hidden" name="note_id" value="{{ note.id }}">
                    
                    <div class="input-group"><input type="text" name="title" value="{{ note.title }}" required></div>
                    <div class="input-group"><textarea name="content">{{ note.content }}</textarea></div>
                    <div class="input-group"><input type="text" name="link" value="{{ note.link }}"></div>
                    
                    <button type="submit" class="btn-submit">Save Changes</button>
                    <button type="button" class="btn-cancel" onclick="toggleEdit('{{ note.id }}')">Cancel</button>
                </form>
            </div>
            
        </div>
        {% endfor %}

        <!-- Add Section Interface (NO PASSWORD REQUIREMENT HERE) -->
        <button class="add-section-btn" id="addBtn" onclick="document.getElementById('addFormContainer').style.display='block'; this.style.display='none';">
            ➕ Add New Section
        </button>

        <div id="addFormContainer" class="display-card" style="display: none;">
            <div class="card-title" style="margin-bottom: 15px;">Create New Section</div>
            <form action="/action" method="POST">
                <input type="hidden" name="action_type" value="add">
                <div class="input-group"><input type="text" name="title" placeholder="Heading (e.g. Work Links)" required></div>
                <div class="input-group"><textarea name="content" placeholder="Type data here..."></textarea></div>
                <div class="input-group"><input type="text" name="link" placeholder="Paste web link here..."></div>
                
                <button type="submit" class="btn-submit">Add to Dashboard</button>
                <button type="button" class="btn-cancel" onclick="document.getElementById('addFormContainer').style.display='none'; document.getElementById('addBtn').style.display='flex';">Cancel</button>
            </form>
        </div>

    </div>

    <script>
        const themeToggleBtn = document.getElementById('themeToggle');
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark');
            themeToggleBtn.innerHTML = '☀️ Light Mode';
        } else {
            document.body.classList.remove('dark');
            themeToggleBtn.innerHTML = '🌙 Dark Mode';
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

        if (!localStorage.getItem('theme')) {
            document.body.classList.add('dark');
            localStorage.setItem('theme', 'dark');
            themeToggleBtn.innerHTML = '☀️ Light Mode';
        }

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
    if not session.get('authenticated'):
        return render_template_string(LOGIN_TEMPLATE, error="")
    return render_template_string(HTML_TEMPLATE, notes=notes, error="", success="")

@app.route('/login', methods=['POST'])
def login():
    pin = request.form.get('pin')
    if pin == MASTER_PIN:
        session['authenticated'] = True
        return redirect(url_for('index'))
    return render_template_string(LOGIN_TEMPLATE, error="❌ Invalid PIN. Please try again.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/action', methods=['POST'])
def handle_action():
    global notes
    if not session.get('authenticated'):
        return redirect(url_for('index'))

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
