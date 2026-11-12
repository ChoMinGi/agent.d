# Cognitive Partner

사용자의 가설과 판단을 근거와 대조하고, 실제 작업 결과에 반영하는 협업 스킬입니다.

**버전:** v1.0.0 · **호스트:** Codex · **라이선스:** 미선택

[설치](#설치) · [사용법](#사용법) · [예시](#예시) · [검증](#검증)

**v1.0.0은 배포 버전입니다. 사고력 향상이나 실무 성과가 입증됐다는 뜻은 아닙니다.**
동작 규칙은 v0.2와 같으며, 평가 자료는 eval-r1의 수정 내용을 유지합니다.

## 소개

AI가 모든 판단을 완성한 뒤 사용자의 승인을 받는 대신, 직접적인 피드백으로 사용자의
가설, 예측, 대안, 검증 기준을 이끌어내고 산출물에 반영합니다.

- 계획, 설계, 디버깅, 조사, 글쓰기에서 함께 검토할 가치가 있는 지점을 찾습니다.
- 이미 제시된 추론은 다시 묻지 않고 활용합니다.
- 사용자와 AI의 판단을 근거에 비추어 수정하고 작업과 검증에 반영합니다.
- 막연한 퀴즈, 프롬프트 점수, 강제적인 찬반 토론은 만들지 않습니다.

단순 작업은 바로 수행하고, 긴급 대응을 훈련 때문에 늦추지 않습니다. 필요한 사실과
답을 숨기지 않으며, AI의 지적이 틀렸다면 수정합니다.

## 설치

로컬 Codex용 안내입니다. 다른 호스트에서의 동작은 검증하지 않았습니다.
설치 단위는 저장소 안의 **`cognitive-partner/` 폴더 전체**입니다.
`evals/`와 평가용 정답은 설치하거나 실행 중 참고할 자료가 아닙니다.

저장소 또는 압축을 푼 루트에서 실행합니다. 기존 설치가 있으면 덮어쓰지 않습니다.

```sh
mkdir -p "$HOME/.agents/skills"
if [ -e "$HOME/.agents/skills/cognitive-partner" ] || [ -L "$HOME/.agents/skills/cognitive-partner" ]; then
  echo "기존 설치가 있습니다. 먼저 비교하고 백업하세요." >&2
else
  cp -R cognitive-partner "$HOME/.agents/skills/cognitive-partner"
fi
```

Codex에서 `$cognitive-partner`로 호출합니다. 감지되지 않으면 Codex를 다시 시작하세요.
자동 선택은 허용하지만 매 대화에서 실행됨을 보장하지는 않습니다.
[설치·제거 안내](docs/install.md)에서 선택적 전역 지침과 제거 방법을 확인할 수 있습니다.

## 사용법

현재 요청과 관련 자료를 함께 제공합니다.

```text
$cognitive-partner 내 요청과 현재 자료에서 중요한 전제나 놓친 관점을 직접 지적해줘.
내가 생각할 가치가 있는 지점 하나를 함께 검토하고, 내 판단을 실제 작업과 검증에 반영해줘.
```

기본 흐름은 **맥락 확인 → 직접 피드백 → 사용자 사고 → 근거와 대조 → 산출물 반영 → 결과 확인**입니다.
추가 질문 자체가 목적이 아니라, 사용자의 생각이 실제 작업에 쓰이는 것이 목적입니다.

## 예시

합성 디버깅 자료에서 반복 횟수는 증가하지만 요청 전송 횟수는 0이라고 가정합니다.
사용자가 재연결을 늘리자고 하면, 연결 문제로 단정할 근거가 부족함을 설명합니다.
사용자가 전송 전 준비 조건을 의심하면 해당 가설을 분기 관측과 재현 실험에 반영합니다.
실제 관측이 가설과 다르면 양쪽의 판단을 수정합니다.

이 예시는 학습 효과의 증거가 아닙니다.
[다중 턴 예시](cognitive-partner/references/examples.md)와
[도움 수준 지침](cognitive-partner/references/intervention-guide.md)을 참고하세요.

## 구성

```text
cognitive-partner/  설치할 스킬: SKILL.md, agents/, references/
docs/              설치, 검증 범위, 게시 절차
evals/             합성 입력과 평가자 전용 기준
audit/             원본 보존 기록과 검증기 계약 검사
scripts/           배포 검사와 게시 도구
integration/       선택적 AGENTS.md 지침 예시
```

설치 파일과 평가 자료를 분리합니다. 게시 도구가 포함되어 있다는 사실은 게시 권한이나
GitHub 업로드 완료를 의미하지 않습니다.

## 검증

저장소 루트에서 Python 3.10 이상으로 실행합니다.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -B validate_package.py
python -B audit/test_validator_contract.py
python -B scripts/check_release.py
```

검사는 LLM을 호출하지 않습니다. 파일, YAML, 평가 자료 계약, 고장 주입, 원본 지침과
배포 파일 목록을 확인합니다. 실제 모델 동작이나 사람의 사고력 향상을 검증하지 않습니다.
28개 합성 사례는 이미 노출된 개발·회귀 자료이며 독립 holdout이 아닙니다.
[평가 계획](evals/PROTOCOL.md)과 [검증 범위](docs/verification.md)를 함께 보세요.

## 제한 사항과 개인정보

- 스킬은 새 도구 권한, 저장 권한, 상시 실행 능력을 부여하지 않습니다.
- 사용자의 동의 없이 전역 설정이나 지속 기억을 변경하지 않습니다.
- 실제 업무 자료, 계정 비밀, 개인 능력 프로필을 공개 저장소에 추가하지 마세요.
- 예제와 정적 검사 통과를 학습 효과나 실무 성능의 증거로 해석하지 마세요.
- 설치·게시·라이선스 선택은 별도 작업입니다. 문서가 준비됐다는 이유로 완료된 것으로 보지 않습니다.

## 문서

- [설치와 제거](docs/install.md)
- [검증 범위](docs/verification.md) · [평가 계획](evals/PROTOCOL.md)
- [변경 기록](CHANGELOG.md) · [릴리스 노트](RELEASE_NOTES.md)
- [게시 절차](docs/publishing.md)
- [README 작성 기준](docs/presentation-guide.md)

## 라이선스

라이선스는 아직 선택하지 않았습니다. [LICENSE](LICENSE)는 소유자가 라이선스를
선택하기 전까지 이용 허락을 부여하지 않는다는 상태 표시입니다.
