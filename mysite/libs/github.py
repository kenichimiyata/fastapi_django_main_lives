import os
import subprocess
import string
import random
import datetime

def github(folder):
    # GitHubユーザー名とトークンを環境変数から取得
    GITHUB_USERNAME = os.getenv("github_user")
    GITHUB_TOKEN = os.getenv("github_token")

    if not GITHUB_USERNAME or not GITHUB_TOKEN:
        print("❌ github_user または github_token が未設定です")
        exit(1)

    # 固定リポジトリ名（既に GitHub 上に存在している必要あり）
    REPO_NAME = "gpt-engeneer"
    controllers_dir = "/home/user/app/controllers"
    target_dir = os.path.join(controllers_dir, folder)

    if not os.path.isdir(target_dir):
        print(f"❌ 指定フォルダが存在しません: {target_dir}")
        exit(1)

    # ランダムなブランチ名を作成（例: folder-20250507-ab12f3）
    def generate_random_string(length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    date_part = datetime.datetime.now().strftime("%Y%m%d")
    branch_name = f"{folder}-{date_part}-{generate_random_string()}"

    # GitHubリポジトリURL
    REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    WEB_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/tree/{branch_name}"

    # コマンド実行関数
    def run_command(command, cwd=None):
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
        if result.returncode != 0:
            print(f"Command failed: {command}\n{result.stderr}")
            exit(1)
        else:
            print(result.stdout)

    # .git がなければ初期化
    if not os.path.isdir(os.path.join(target_dir, ".git")):
        run_command("git init", cwd=target_dir)
        run_command(f"git remote add origin {REPO_URL}", cwd=target_dir)
        print("📁 git 初期化と origin 追加")

    # 現在の変更をクリーンにする
    run_command("git reset", cwd=target_dir)

    # 新しいブランチを作成して移動
    run_command(f"git checkout -b {branch_name}", cwd=target_dir)

    # ステージングとコミット
    run_command("git add -f .", cwd=target_dir)
    run_command(f'git commit -m "Initial commit on branch {branch_name}"', cwd=target_dir)

    # 機密ファイル（githubs.shなど）を履歴から削除
    os.environ['FILTER_BRANCH_SQUELCH_WARNING'] = '1'
    run_command("git filter-branch --force --index-filter "
                '"git rm --cached --ignore-unmatch githubs.sh" '
                "--prune-empty --tag-name-filter cat -- --all", cwd=target_dir)

    # push 先の origin がなければ追加（すでにチェック済みだが念のため）
    remotes = subprocess.run("git remote", shell=True, text=True, capture_output=True, cwd=target_dir)
    if "origin" not in remotes.stdout:
        run_command(f"git remote add origin {REPO_URL}", cwd=target_dir)

    # ブランチを push（強制ではなく通常pushでOK）
    run_command(f"git push -u origin {branch_name}", cwd=target_dir)

    print(f"✅ Successfully pushed to GitHub branch: {branch_name}")
    print(f"🔗 {WEB_URL}")
    return WEB_URL

# 使用例
# 
# github_branch("test_folders")
