import os
import subprocess
import time

# ------------------- 당신이 수정해야 할 부분 ------------------- #

# 1. 깃허브 아이디를 입력하세요.
GITHUB_USERNAME = "kk01111789-cell"

# 2. 깃허브 저장소 이름을 입력하세요.
REPO_NAME = "soa" 

# 3. 이미지들이 모여있는 로컬 폴더 경로를 입력하세요.
# 예: "C:/Users/MyUser/Desktop/my-images"
# 경로의 \는 /로 바꿔주세요.
IMAGE_SOURCE_FOLDER = "C:/Download/image2"

# ----------------------------------------------------------- #


def run_command(command):
    """주어진 명령어를 터미널에서 실행합니다."""
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    # 스크립트가 있는 저장소 폴더로 작업 위치를 변경합니다.
    repo_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_folder)

    # 이미지 폴더에서 모든 파일을 저장소 폴더로 복사
    print(f"\nStep 1: Copying files from {IMAGE_SOURCE_FOLDER}...")
    for filename in os.listdir(IMAGE_SOURCE_FOLDER):
        source_path = os.path.join(IMAGE_SOURCE_FOLDER, filename)
        if os.path.isfile(source_path):
            # os.system을 사용하여 파일 복사 (윈도우, 맥, 리눅스 호환)
            os.system(f'copy "{source_path}" "{repo_folder}"' if os.name == 'nt' else f'cp "{source_path}" "{repo_folder}"')
    
    print("\nStep 2: Uploading to GitHub...")
    
    # 깃허브에 업로드 (add, commit, push)
    if not run_command(["git", "add", "."]): return
    
    commit_message = f"Add images batch {time.strftime('%Y-%m-%d %H:%M:%S')}"
    if not run_command(["git", "commit", "-m", commit_message]): return

    if not run_command(["git", "push"]): return

    print("\nStep 3: Generating public URLs...")
    
    # 링크를 저장할 파일
    links_file_path = os.path.join(repo_folder, "links.txt")
    
    with open(links_file_path, "w") as f:
        f.write("--- Generated Image Links ---\n")
        # 현재 폴더의 이미지 파일 목록을 기준으로 링크 생성
        image_files = [file for file in os.listdir(repo_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        for filename in sorted(image_files):
            # raw.githubusercontent.com 링크 생성
            url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{filename}"
            
            # 프롬프트에 바로 쓸 수 있는 마크다운 형식으로 저장
            markdown_link = f"{os.path.splitext(filename)[0]}: {url}"
            print(markdown_link)
            f.write(markdown_link + "\n")

    print(f"\n\n🔥🔥🔥 All Done! 🔥🔥🔥")
    print(f"All links have been saved to: {links_file_path}")


if __name__ == "__main__":
    main()