# 05-conventions.md

## 명명 규칙
- 백엔드: snake_case
- 프론트엔드: camelCase
- 컴포넌트: PascalCase
- 식별자는 영어로 작성한다. 주석만 한국어로 작성한다.

## 금지 사항 (5개)

| 금지 | 이유 | 대안 |
|---|---|---|
| print 디버깅 | 노이즈 발생, 운영 환경 관리 어려움 | logging 모듈 사용 |
| bare except | 예외를 삼켜 문제를 숨김 | except SpecificError 처럼 구체적으로 명시 |
| 비밀번호 하드코딩 | 보안 사고 위험 | .env + os.getenv 사용 |
| any 타입 (TS) | 타입 의미 상실 | 명시적 타입 지정 |
| !important | CSS 우선순위 꼬임 | 셀렉터 구조 개선 |

## .gitignore
다음 항목을 포함한다:
```
__pycache__/
.venv/
*.db
*.log
```

## 테스트 매트릭스

| 케이스 | 요청 | 기대 응답 |
|---|---|---|
| 정상 생성 | POST title만 | 201 |
| 목록 | GET /api/tasks | 200, description 없음 |
| 단건 | GET /api/tasks/{id} | 200, description 있음 |
| 수정 | PUT 전 필드 | 200 |
| 삭제 | DELETE | 204 |
| title 누락 | POST title 없음 | 400 |
| status 오값 | POST/PUT status 잘못된 값 | 400 |
| due_at 형식 오류 | POST/PUT due_at 잘못된 형식 | 400 |
| 없는 id | GET/PUT/DELETE 존재하지 않는 id | 404 |
| 스펙 외 필드 | POST/PUT 정의되지 않은 필드 포함 | 422 |

## git 커밋 규칙
커밋 메시지는 `feat/fix/docs/refactor/test/chore` 접두사 + 한국어 요약 형식을 따른다.
예: `docs: Phase 1 설계 문서 7종 작성`
