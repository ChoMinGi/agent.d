# DecisionGuard

현재 프로젝트의 결정과 확인된 인수인계를 다음 조사·설계·QA 작업에 반영하는 스킬입니다.

**버전:** v0.6.1 · **호스트:** Codex 중심 Agent Skill · **라이선스:** MIT

[설치](#설치) · [사용법](#사용법) · [예시](#예시) · [검증](#검증)

**실험적 알파입니다.** 정확도 향상, 사용자 수정 감소, 시간 절약은 입증되지 않았습니다.
호스트 에이전트가 수행할 작업 흐름을 정의하며, 독립적으로 실행되는 지식 서비스가 아닙니다.

## 소개

이전 프로젝트의 선택이 다음 작업에 영향을 줄 때 사용합니다. 일반적인 문서 요약에는
이 흐름이 필요하지 않을 수 있습니다. 결과물은 사용자가 요청한 작업이며, 전체 추출표나
감사 자료는 선택 사항입니다.

- 관련 자료에서 결정의 권한과 적용 범위를 확인합니다.
- 확인된 인수인계를 재사용하기 전에 현재 자료와 다시 대조합니다.
- 승인된 변경을 설계와 QA 기준에 반영합니다.
- 초안, 가설, 승인된 선택, 실제 테스트 결과를 구분합니다.
- 기억이나 Notion에 저장할 때는 정확한 변경안을 보여 주고 확인받습니다.

## 설치

설치 단위는 **`skills/decisionguard/` 폴더 전체**입니다. Codex에 다음과 같이 요청합니다.

```text
$skill-installer install https://github.com/ChoMinGi/decisionguard-skill/tree/main/skills/decisionguard
```

호스트가 감지하면 다음 턴부터 사용할 수 있습니다. 나타나지 않으면 Codex를 다시 시작하세요.
[설치·업데이트 안내](docs/install.md)에 고정 버전, 수동 설치, 다른 호스트와 제거 방법이 있습니다.
다른 호스트의 커넥터 호환성은 인증되지 않았습니다.

실제 Notion 자료를 쓰려면 호스트에서 Notion을 연결하고 프로젝트 범위를 지정해야 합니다.
프롬프트에 인증 정보를 넣지 마세요. 아래 가상 예제는 Notion 연결 없이 사용할 수 있습니다.
선택적 로컬 도구는 Python 3.10 이상과 표준 라이브러리만 필요합니다.

## 사용법

프로젝트나 자료 위치를 지정하고, 수행할 작업을 요청합니다.

```text
$decisionguard 이전에 확인한 판단과 현재 프로젝트 문서를 대조해서
다음 기능의 QA 계획을 작성해줘. 바뀐 결정은 테스트 기준에 반영하고,
아직 실행하지 않은 테스트는 구분해줘. 노션은 읽기 전용으로 확인해.
```

영어로도 요청할 수 있습니다.

```text
Use $decisionguard to draft the feature design from this project's current
sources. Recheck the confirmed handoff if available, apply accepted changes,
and identify unresolved inputs that affect this design. Keep Notion read-only.
```

기억은 실제로 확인된 위치에 저장했고 다음 에이전트가 그 위치에 접근할 수 있을 때만
작업 간에 이어집니다. 스킬 설치만으로 프로젝트 이력을 가져오거나 자료 접근 권한이 생기지 않습니다.

## 예시

가상의 ReadingLight 도서관 시범 사업에서 개별 좌석 지도 대신 공간별 혼잡도 구간을
표시하기로 합니다. 이후 설계 초안이 옛 좌석 지도를 다시 제안하고, QA에서는 분석 이벤트에
좌석 단위 정보가 여전히 전송되는 것을 발견합니다.

| 작업 | 기대하는 대응 |
| --- | --- |
| 조사 | 작은 현장 관측을 활용하되 전체 시장 수요로 확대 해석하지 않습니다. |
| 변경 승인 후 설계 | 공간별 표시 결정을 적용하고, 승인되지 않은 새 좌석 지도 초안은 구분합니다. |
| QA | 개인정보 검사 실패, 미실행 접근성 검사, 누락된 출시 승인을 구분합니다. |

[가상 프로젝트 따라 하기](docs/walkthrough.md)에 짧은 원자료 3개와 복사 가능한 요청이 있습니다.
등장하는 사람, 조직, 사건은 모두 창작입니다. 작업 흐름의 예시이며 일반 성능의 증거가 아닙니다.

## 구성

```text
skills/decisionguard/  설치할 스킬: SKILL.md, agents/, references/, scripts/
docs/                  설치, 사용 예시, 평가와 유지보수 안내
examples/              가상 프로젝트와 봉인된 평가 기록
scripts/               오프라인 평가와 배포 검사
tests/                 로컬 도구 회귀 테스트
MANIFEST.txt           배포에 포함할 파일 목록
```

실제 프로젝트의 내보내기, 기억 원장, 승인 기록과 보고서는 공개 소스 트리 밖에 보관합니다.

## 검증

저장소 루트에서 Python 3.10 이상으로 실행합니다.

```sh
python3 -B -m unittest discover -s tests
python3 -B scripts/evaluate_handoff.py
python3 -B scripts/release_check.py
```

테스트는 로컬 도구의 동작과 근거 무결성을 확인합니다. 가상 평가 기록을 모델 호출 없이
재실행할 수 있지만, 재실행은 새로운 모델 평가가 아닙니다.
[평가 상세](docs/evaluation.md), [인수인계 평가의 한계](docs/handoff-evaluation.md),
[유지보수 검사](docs/release.md)를 참고하세요.

초기 게시본에는 GitHub Actions가 활성화되어 있지 않습니다.
[선택적 워크플로 예시](docs/ci.example.yml)를 제공합니다.

## 제한 사항과 개인정보

- 검색과 해석은 호스트 에이전트가 수행합니다. 도구는 입력 기록을 검사할 뿐, 주장의 진실성,
  검색의 완전성, 승인자의 권한을 증명하지 않습니다.
- 자료 접근 권한과 실제 확인 절차는 호스트가 지켜야 합니다.
- 조건부 쓰기가 없는 커넥터에서는 다시 읽고 확인해도 동시 편집 위험을 없앨 수 없습니다.
- 예제는 고객 자료를 익명화한 것이 아니라 처음부터 창작한 자료입니다.
- 실제 내보내기, 기억 원장, 승인 기록과 보고서는 공개 저장소에 넣지 마세요.

자세한 경계는 [보안과 개인정보 안내](SECURITY.md)에 있습니다.

## 문서

- [설치와 첫 사용](docs/install.md) · [가상 프로젝트 따라 하기](docs/walkthrough.md)
- [평가 상세](docs/evaluation.md) · [인수인계 평가](docs/handoff-evaluation.md)
- [릴리스 노트](docs/release-notes.md) · [유지보수 검사](docs/release.md)
- [기여 안내](CONTRIBUTING.md) · [보안과 개인정보](SECURITY.md)
- [README 작성 기준](docs/presentation-guide.md)

피드백은 [Issues](https://github.com/ChoMinGi/decisionguard-skill/issues)에 남길 수 있습니다.
작업, 스킬의 실제 동작, 필요했던 수정을 작은 **가상 재현 사례**로 설명해 주세요.

## 라이선스

[MIT](LICENSE). Notion 또는 OpenAI와의 제휴를 의미하지 않습니다.
