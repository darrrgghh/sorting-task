# Vocal Similarity Sorting Task

Интерфейс для задачи свободной сортировки аудиостимулов. Предназначен для встраивания в Qualtrics через iframe и деплоя на Vercel.

## Структура проекта

```
sorting-task/
├── index.html          # Основная страница с drag-and-drop
├── config.js           # Настройки: список стимулов, URL аудио
├── package.json        # npm scripts для локального запуска
├── vercel.json         # Конфиг для Vercel
├── README.md           # Этот файл
├── QUALTRICS_SETUP.md  # Инструкция по интеграции с Qualtrics
└── audio/              # Папка с WAV-файлами
    ├── SMPC-01.wav
    ├── SMPC-02.wav
    └── ...
```

## Локальный просмотр

```bash
cd sorting-task
npm run dev
```

Откройте **http://localhost:3000** в браузере. Аудио работает только через локальный сервер (не через file://).

## Быстрый старт

### 1. Подготовка аудио

- Положите WAV-файлы в папку `audio/`.
- Имена: `SMPC-01.wav`, `SMPC-02.wav`, … `SMPC-27.wav`.

### 2. Настройка config.js

Отредактируйте `config.js`:

- `AUDIO_BASE_URL` — базовый URL для аудио:
  - Для Vercel с папкой `public/audio`: `"/audio"`
  - Для внешнего хостинга: `"https://example.com/audio"`
- `STIMULI` — список стимулов (id и отображаемое имя).

### 3. Деплой на Vercel

**Вариант A: Через GitHub**

1. Создайте новый репозиторий.
2. Скопируйте содержимое папки `sorting-task` в корень репо.
3. На [vercel.com](https://vercel.com) → New Project → Import из GitHub.
4. Deploy. Получите URL вида `https://your-project.vercel.app`.

**Вариант B: Через CLI**

```bash
cd sorting-task
npx vercel
```

Следуйте подсказкам. Папка `audio` должна быть в корне — Vercel отдаёт статические файлы из корня.

**Важно:** Если аудио в `audio/`, путь будет `https://your-project.vercel.app/audio/SMPC-01.wav`. В `config.js` укажите `AUDIO_BASE_URL = "/audio"`.

### 4. Интеграция с Qualtrics

Подробная инструкция в **[QUALTRICS_SETUP.md](./QUALTRICS_SETUP.md)**.

Кратко:
1. Добавить блок с iframe, указывающий на ваш Vercel URL.
2. Добавить Embedded Data: `sorting_result`, `sorting_compact`.
3. Добавить JavaScript, который слушает `postMessage` от iframe и сохраняет данные в Qualtrics.

---

## Как это работает

### Интерфейс

- **Слева:** список стимулов с кнопкой Play у каждого.
- **Справа:** группы. Участник перетаскивает стимулы в группы, может добавлять новые группы.
- **Кнопка Done:** отправляет результат в Qualtrics (если страница в iframe) и переводит на следующий блок.

### Передача данных в Qualtrics

1. Участник нажимает «Done».
2. Страница формирует объект с группами и вызывает `window.parent.postMessage(...)`.
3. Qualtrics (родительское окно) получает сообщение через `window.addEventListener('message', ...)`.
4. Скрипт в Qualtrics сохраняет данные в Embedded Data и нажимает «Далее».

### Формат результата

- **compact:** `SMPC-01,SMPC-02|SMPC-03,SMPC-04|SMPC-05` — группы разделены `|`, элементы в группе — запятой.
- **groups:** JSON-массив массивов, например `[["SMPC-01","SMPC-02"],["SMPC-03","SMPC-04"]]`.

---

## Альтернативный локальный запуск

```bash
npx serve . -p 3000
# или
python -m http.server 3000
```
