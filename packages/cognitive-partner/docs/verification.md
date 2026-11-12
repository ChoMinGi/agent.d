# 검증 범위

## 현재 확인할 수 있는 것

`validate_package.py`는 패키지 구조, 버전, YAML, 참조 파일, 합성 평가 자료 형식을 검사합니다.
`audit/test_validator_contract.py`는 정상/잘못된 자료형, 순서 변경, 손상 주입, 규칙 보존을 검사합니다.
실행 결과는 `validation-report.json`과 `audit/validator-contract-results.json`에 저장됩니다.
실행 횟수나 assertion 수는 독립적인 업무 과제 수 또는 행동 성공률이 아닙니다.

## 1.0.0에서 달라진 것

핵심 지침에서는 버전 메타데이터만 0.2.0에서 1.0.0으로 바뀝니다. 나머지 5개 행동 관련
파일은 바이트 단위로 같습니다. `audit/release-provenance.json`에 원본과 현재 해시가 있습니다.
검증기는 새 버전을 검사하며, 원본 보존 검사는 버전 한 줄만 정규화해서 비교합니다.

## 확인하지 않은 것

실제 호스트 로딩, 자동 선택의 신뢰도, 깨끗한 모델 세션의 비교 실험, 사용자 사고력 향상,
새 과제로의 일반화, 과적합 해소는 미검증입니다. 이번 배포에 LLM 호출은 포함되지 않습니다.
기존 28개 사례와 2개 자료 부재 대조군은 개발 자료이며 독립 holdout으로 부르지 않습니다.

`audit/history/eval-r1/`와 `audit/patch-log.json`은 이전 평가 수정의 기록입니다.
이전 버전 숫자와 결과를 현재 실행의 성능으로 소급 변경하지 않았습니다.

## 이번 로컬 재검증 (2026-11-12)

ChatGPT Library에서 내려받은 v0.2, v0.2-eval-r1, v1.0.0 전체 배포본과
Skill 설치본을 직접 대조했습니다. 네 ZIP의 CRC 검사는 모두 통과했습니다.
v1.0.0의 `SKILL.md`는 버전 표기를 0.2.0으로 되돌리면 v0.2와 바이트 단위로
일치합니다. 나머지 다섯 행동 관련 파일도 v0.2 및 eval-r1과 일치합니다.
평가 입력 세 파일은 eval-r1과 일치하고, 설치본의 다섯 파일은 전체 배포본의
같은 파일과 일치합니다.

이 환경에서 `validate_package.py`는 152개 정적 검사에 통과했고,
`audit/test_validator_contract.py`는 158/158개 계약 검사에 통과했습니다.
`scripts/check_release.py`와 Agent Skills `quick_validate.py`도 통과했습니다.
이는 구조와 평가 데이터 계약의 검증이며 모델 행동이나 사용자 사고력 개선의 증거가 아닙니다.
이번 배포본에는 라이선스 선택 보류를 명시하는 `LICENSE` 파일을 추가했습니다.
