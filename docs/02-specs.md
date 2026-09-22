# 02-specs.md (WHAT)

## Task 모델 필드 (7개)

| 순서 | 필드명 | 타입 | 설명 |
|---|---|---|---|
| 1 | id | INTEGER, PK, AUTOINCREMENT | 자동 증가 |
| 2 | title | VARCHAR(200) | 필수 |
| 3 | description | TEXT | 선택 |
| 4 | status | todo / in_progress / done | 기본값 `todo` |
| 5 | due_at | DATETIME (UTC) | 선택 |
| 6 | created_at | DATETIME | 서버 자동 생성 |
| 7 | updated_at | DATETIME | 서버 자동 갱신 |

## 검증
- `title` / `status` / `due_at` 형식 위반 → 400
- 존재하지 않는 id → 404
- 스펙에 없는 필드가 오면 → 422로 거부한다 (조용히 무시 금지)
- `due_at`은 UTC로 저장하고, 화면에서 로컬 시간으로 변환하여 표시한다
- 응답의 날짜 세 필드(`due_at`, `created_at`, `updated_at`)는 UTC ISO 8601 형식으로 통일한다

## REST API (5개, `/api/` 접두사 필수)

| Method | 경로 | 성공 응답 코드 |
|---|---|---|
| POST | /api/tasks | 201 |
| GET | /api/tasks | 200 |
| GET | /api/tasks/{id} | 200 |
| PUT | /api/tasks/{id} | 200 |
| DELETE | /api/tasks/{id} | 204 |

- 목록(GET /api/tasks) 응답에는 `description`을 제외한다
- 단건(GET /api/tasks/{id}) 응답에는 `description`을 포함한다

## 화면 명세

### 1. 추가 화면 - 폼

| 필드 | 설명 |
|---|---|
| title | 텍스트 입력, 필수 |
| due_at | 날짜+시간 선택 |
| status | 선택 드롭다운 |

### 2. 목록 화면 - 카드

| 요소 | 설명 |
|---|---|
| status 배지 | 상태별 색상 구분 표시 |
| 마감까지 남은 시간 | due_at 기준 남은 시간 표시 |

### 3. 수정 화면 - 모달

| 트리거 | 동작 |
|---|---|
| 카드 클릭 | 모달 오픈, 전 필드(title/description/status/due_at) 수정 가능 |

### 4. 삭제 화면

| 트리거 | 동작 |
|---|---|
| 휴지통 아이콘 클릭 | 확인창 표시 → 확인 시 DELETE 요청 |
