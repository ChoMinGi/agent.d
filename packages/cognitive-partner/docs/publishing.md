# GitHub 게시

이 단계는 원격 쓰기입니다. 현재 배포 준비 과정에서는 실행하지 않았습니다.
대상은 `ChoMinGi/cognitive-partner`, 태그는 `v1.0.0`입니다.
Git, GitHub CLI(`gh`), Python 3.10+, PyYAML, Git 작성자 설정이 필요합니다.
`gh auth login`으로 해당 계정에 로그인하세요. 토큰을 프롬프트에 붙여넣지 마세요.

```sh
bash scripts/publish.sh --dry-run
bash scripts/publish.sh --private
```

공개 게시를 직접 결정했다면 `--private` 대신 `--public`을 사용할 수 있습니다.
기본은 비공개이며 스크립트는 기존 저장소나 기존 Git 작업 트리를 재사용하지 않습니다.
라이선스는 소유자가 별도로 결정하세요.

스크립트는 로컬 검증 후 초기 커밋을 만들고, 새 저장소를 생성해 커밋을 올린 다음
`v1.0.0` 태그와 GitHub Release를 만듭니다. 강제 푸시나 기존 릴리스 덮어쓰기는 하지 않습니다.
중간 실패 시 이미 생성된 원격 저장소는 자동 삭제하지 않습니다. 해당 상태를 확인한 뒤 수동으로 이어가세요.

공식 명령 참조:
- https://cli.github.com/manual/gh_repo_create
- https://cli.github.com/manual/gh_release_create
