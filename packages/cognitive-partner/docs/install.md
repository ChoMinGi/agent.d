# 설치와 제거

이 안내는 로컬 Codex 설치용입니다. 다른 호스트에서의 동작은 검증하지 않았습니다.
공식 문서: https://learn.chatgpt.com/docs/build-skills

저장소 또는 압축을 푼 루트에서 실행합니다. 기존 설치가 있으면 덮어쓰지 않고 중단합니다.

```sh
mkdir -p "$HOME/.agents/skills"
if [ -e "$HOME/.agents/skills/cognitive-partner" ] || [ -L "$HOME/.agents/skills/cognitive-partner" ]; then
  echo "기존 설치가 있습니다. 먼저 비교하고 백업하세요." >&2
else
  cp -R cognitive-partner "$HOME/.agents/skills/cognitive-partner"
fi
```

Codex에서 `$cognitive-partner`를 명시하여 호출합니다. 자동 선택도 허용되어 있으나
매 대화에서 실행됨을 보장하지 않습니다. 감지되지 않으면 Codex를 다시 시작하세요.

`integration/AGENTS.snippet.md`는 선택 사항입니다. 기존 전역 지침을 덮어쓰지 말고,
내용과 적용 범위를 검토한 뒤 필요한 부분만 병합하세요. 평가용 정답은 설치하지 마세요.

제거할 때는 설치한 `cognitive-partner` 폴더만 제거하고, 직접 추가한 전역 지침도 별도로
검토해 제거하세요. 이 저장소에 있는 원본이나 다른 Skill 폴더를 삭제할 필요는 없습니다.
