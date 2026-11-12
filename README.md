# agent.d

> My working habits, packaged as agent skills.

AI와 함께 문제를 검토하고, 프로젝트의 결정을 이어가고, 만든 기능을 보여주기 위한 개인 스킬 모음입니다.

**Question assumptions. Keep decisions grounded. Show the work.**

## The kit

| Skill | 언제 쓰나요? | Host |
|---|---|---|
| [Cognitive Partner](packages/cognitive-partner/README.md) | 문제의 전제와 근거를 검토하고, 내 판단을 설계와 작업에 반영할 때 | Codex |
| [DecisionGuard](packages/decisionguard/README.md) | 이전에 확인한 결정을 현재 자료와 대조해서 다음 조사, 설계, QA에 이어갈 때 | Codex 중심 |
| [Web Feature Demo](packages/web-feature-demo/README.md) | 로컬 웹 기능을 설명과 하이라이트로 시연하고, 필요하면 영상으로 남길 때 | Claude Code / macOS |

각 스킬은 필요한 작업에서 개별적으로 선택해 사용합니다.

## Why these skills?

AI와 작업하면서 반복해서 필요했던 습관을 스킬로 정리했습니다.

- **판단을 구체화하기.** 중요한 전제와 대안을 검토하고, 내가 내린 판단을 실제 결과물에 반영합니다.
- **결정을 이어가기.** 무엇을 왜 선택했는지 현재 근거와 다시 대조하고, 다음 작업의 기준으로 사용합니다.
- **결과를 보여주기.** 구현한 기능을 사람이 따라갈 수 있는 장면과 설명으로 전달합니다.

## Try one

**설계의 전제를 함께 검토하고 싶을 때**

```text
$cognitive-partner 이 설계에서 근거가 약한 전제와 놓친 대안을 짚어줘.
내가 판단할 지점을 함께 검토하고, 그 판단을 설계와 검증 계획에 반영해줘.
```

**프로젝트의 결정이 다음 작업에도 반영되어야 할 때**

```text
$decisionguard 이전에 확인한 결정과 현재 프로젝트 문서를 대조해서
이번 기능의 QA 계획을 작성해줘. 바뀐 결정과 아직 확인하지 못한 부분을 구분해줘.
```

**만든 기능을 직접 보여주고 싶을 때**

```text
/web-feature-demo http://localhost:3000
이번에 바뀐 회원가입 흐름을 설명하면서 보여줘. 영상도 저장해줘.
```

## Setup & docs

위 스킬 이름을 누르면 각 패키지의 설치 방법, 사용 예시, 지원 환경과 검증 범위를 확인할 수 있습니다.

설치 단위와 실행 환경은 스킬마다 다릅니다. 라이선스도 각 패키지의 안내를 따릅니다.

- [이 모노레포에서 개별 설치하기](docs/install.md)
- [구조, 독립 버전과 원본 저장소](docs/maintenance.md)
- [검증 결과와 한계](docs/verification.md)
- [라이선스와 외부 구성 요소](LICENSE.md)

Cognitive Partner의 라이선스는 아직 선택하지 않았습니다. DecisionGuard와 Web Feature Demo는 각 패키지의 MIT 고지를 유지합니다. 이 모음은 사고력 향상, 프로젝트 정확도 향상, 서비스의 기능 테스트 통과를 보장하지 않습니다.
