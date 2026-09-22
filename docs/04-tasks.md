# 04-tasks.md

## 진행 규칙
- 순서대로만 진행한다 (병렬 금지)
- 단계별 검증 필수 — 검증 통과 전에는 다음 단계로 넘어가지 않는다
- Phase 이름과 개수는 아래 3개로 고정한다 (변경 금지)
- 이후 "backend 진행해" = Phase 2 전체 실행, "frontend 진행해" = Phase 3 전체 실행

---

## Phase 1 (설계): CLAUDE.md + docs/ 6종 작성

| 단계 | 검증 방법 | 완료 |
|---|---|---|
| 1. CLAUDE.md 작성 | 역할/스택/절차/절대규칙 4섹션 존재 확인 | [x] |
| 2. docs/ 폴더 및 6개 파일 생성 | 파일명 6개 정확히 일치하는지 확인 | [x] |
| 3. 00-overview.md 작성 | 매핑표·읽는 순서·분리 이유 포함 확인 | [x] |
| 4. 01-product.md 작성 | 목표·페르소나·MVP 범위 포함 확인 | [x] |
| 5. 01-product.md 성공 기준 추가 | 4개 성공 기준 항목 확인 | [x] |
| 6. 02-specs.md 작성 | Task 필드 7개·API 5개·화면 4종 확인 | [x] |
| 7. 03-design.md 작성 | 8행 표 + 의존성 정책 확인 | [x] |
| 8. 04-tasks.md 작성 | Phase 1/2/3 체크리스트 존재 확인 | [x] |
| 9. 05-conventions.md 작성 | 명명 규칙·금지·구현 규칙·git 컨벤션 확인 | [x] |
| 10. CLAUDE.md ↔ docs 파일명 일치 확인 | 6개 파일명·순서 동일한지 재확인 | [x] |

---

## Phase 2 (백엔드): backend/ FastAPI → CRUD API 5개 → Swagger 확인

허용 의존성: `fastapi`, `uvicorn`, `sqlalchemy`, `pytest`, `httpx` (이 외 추가 금지)

| 단계 | 검증 방법 | 완료 |
|---|---|---|
| 1. backend/ 폴더 및 가상환경 준비 | 폴더 생성 확인 | [x] |
| 2. 의존성 설치 (5종 한정) | requirements 파일에 5종만 존재 | [x] |
| 3. SQLAlchemy 모델 정의 (Task, 필드 7개) | 02-specs.md 필드와 일치 확인 | [x] |
| 4. DB 세션/초기화 코드 작성 | 앱 실행 시 SQLite 파일 생성 확인 | [x] |
| 5. POST /api/tasks 구현 | 201 응답 + 422(스펙 외 필드) 확인 | [x] |
| 6. GET /api/tasks 구현 | 200 응답, description 제외 확인 | [x] |
| 7. GET /api/tasks/{id} 구현 | 200/404 응답, description 포함 확인 | [x] |
| 8. PUT /api/tasks/{id} 구현 | 200/400/404 응답 확인 | [x] |
| 9. DELETE /api/tasks/{id} 구현 | 204/404 응답 확인 | [x] |
| 10. pytest로 5개 API 테스트 작성 및 Swagger(/docs) 확인 | 테스트 전부 통과 + Swagger UI 정상 노출 | [x] |

---

## Phase 3 (프론트): frontend/ HTML+JS+Tailwind → 화면 → API 연결 → git push

Phase 2 완료 (2026-09-22): CRUD API 5개, pytest 10종 통과, 날짜 3필드 UTC ISO 8601 표준 라이브러리로 통일.

| 단계 | 검증 방법 | 완료 |
|---|---|---|
| 1. frontend/ 폴더 및 index.html, app.js 생성 | 2개 파일만 존재 확인 | [x] |
| 2. Tailwind CDN + Mac OS 톤 레이아웃 구성 | 둥근 모서리/그림자/반투명 카드 확인 | [x] |
| 3. 추가 폼 화면 구현 | title/due_at/status 입력 후 POST 동작 확인 | [x] |
| 4. 목록 카드 화면 구현 | status 배지 + 남은 시간 표시 확인 | [x] |
| 5. 수정 모달 구현 | 카드 클릭 → 모달 → PUT 동작 확인 | [x] |
| 6. 삭제 기능 구현 | 휴지통 → 확인 → DELETE 동작 확인 | [x] |
| 7. 테마 토글 + 반응형(360px) 적용 | localStorage 저장 확인, 360px에서 미깨짐 확인 | [x] |
| 8. 전체 동작 확인 후 git push | 새로고침 데이터 유지 + CRUD 4종 동작 확인 후 push (API 레벨 curl 확인, 브라우저 시각 확인 제외) | [x] |
