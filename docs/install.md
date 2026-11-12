# 개별 설치

세 스킬을 한 번에 활성화하지 않습니다. 필요한 스킬만 복사하세요. Python 3.10 이상을 사용합니다. 명령은 `agent.d` 루트에서 실행하며, 기존 설치와 심볼릭 링크는 덮어쓰지 않습니다.

## Codex

```sh
mkdir -p "$HOME/.agents/skills"
python3 -B scripts/install_skill.py --skill cognitive-partner --dest "$HOME/.agents/skills/cognitive-partner"
# 또는 DecisionGuard만 설치
python3 -B scripts/install_skill.py --skill decisionguard --dest "$HOME/.agents/skills/decisionguard"
```

설치 뒤 `$cognitive-partner` 또는 `$decisionguard`로 호출합니다. 감지되지 않으면 호스트의 스킬 설정을 확인하고 재시작하세요. 호스트의 실행과 자동 선택은 정적 설치 검사로 인증되지 않습니다.

## Claude Code

```sh
mkdir -p "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
python3 -B scripts/install_skill.py --skill web-feature-demo --dest "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/web-feature-demo"
```

Claude Code를 다시 시작하고 `/web-feature-demo`를 호출합니다. Node.js 20 이상, Google Chrome, 로컬 서비스가 필요합니다. 브라우저 실행기 설치와 다운로드는 이 복사 단계에서 수행하지 않습니다. 상세 설정과 주의 사항은 [패키지 README](../packages/web-feature-demo/README.md)를 확인하세요.

## 설치 내용과 업데이트

- Cognitive Partner: `packages/cognitive-partner/cognitive-partner/` 전체와 패키지 LICENSE. 평가자 전용 자료는 설치하지 않습니다.
- DecisionGuard: `packages/decisionguard/skills/decisionguard/` 전체와 패키지 LICENSE. 예제 프로젝트와 평가 기록은 설치하지 않습니다.
- Web Feature Demo: `packages/web-feature-demo/` 전체. 원본의 독립 설치 구조를 유지합니다.

`--dry-run`을 추가하면 대상 경로와 파일 목록만 출력합니다. `--dest`의 부모 폴더는 먼저 만들어 두세요. 대상 이름은 스킬 이름과 같아야 합니다. 복사 오류가 나면 부분 설치 폴더를 남기므로 검사한 뒤 처리하세요.

기존 설치는 직접 비교하고 백업한 뒤 새 경로에 설치해 교체하세요. 자동 삭제, 덮어쓰기, 전역 지침 변경, 인증 설정 변경은 하지 않습니다. 제거할 때는 자신이 설치한 복사본만 제거하며 프로젝트 자료와 기억은 별도입니다.

원본 패키지 문서의 기존 GitHub 설치 링크는 그대로 유지했습니다. 이 모노레포를 사용하려면 위 명령을 사용하세요. 아직 생성되지 않은 모노레포 URL을 설치 가능한 주소로 안내하지 않습니다.

## 독립 ZIP 만들기

```sh
mkdir -p dist
python3 -B scripts/package_skill.py --skill decisionguard --out dist/decisionguard-v0.6.1.zip
```

`--skill`을 바꾸면 각 스킬을 따로 만들 수 있습니다. ZIP 내부 최상위 폴더는 스킬 이름이며 LICENSE를 포함합니다. 이미 있는 출력 파일은 덮어쓰지 않습니다. Cognitive Partner는 라이선스 미선택 상태를 그대로 담으며, ZIP 생성은 공개 배포 허락을 의미하지 않습니다.
