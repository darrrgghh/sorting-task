# Интеграция с Qualtrics

## 1. Встраивание страницы в опрос

### Шаг 1: Добавить блок с iframe

1. В Qualtrics создайте новый блок (Block) для задачи сортировки.
2. Добавьте вопрос типа **Descriptive Text**.
3. Включите **Rich Content Editor** и перейдите в режим **HTML** (иконка `</>`).
4. Вставьте код:

```html
<div id="sorting-container" style="min-height: 750px;">
  <iframe
    id="sorting-iframe"
    src="https://ВАШ-ПРОЕКТ.vercel.app/"
    style="width: 100%; height: 750px; border: none; border-radius: 8px;"
    title="Sorting Task"
  ></iframe>
</div>
<p id="sorting-status" style="color: #666; font-size: 13px;">Complete the sorting task above, then click "Done" to continue.</p>
```

Чтобы увеличить область: измените `height` (например, 800px или 80vh для ~80% высоты экрана).

Замените `https://ВАШ-ПРОЕКТ.vercel.app/` на ваш реальный URL с Vercel.

---

### Шаг 2: Добавить Embedded Data

1. В настройках опроса: **Survey flow** → **Add a new element** → **Embedded Data**.
2. Добавьте поля:
   - `sorting_result` (JSON с группами)
   - `sorting_compact` (компактная строка для экспорта)
   - `sorting_mapping` (соответствие Stimulus 01–27 → SMPC-xx)

---

### Шаг 3: Добавить JavaScript для приёма данных

1. В блоке с iframe: **Add JavaScript** (в настройках блока или вопроса).
2. Вставьте код:

```javascript
Qualtrics.SurveyEngine.addOnload(function() {
  var that = this;
  
  window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'SMPC_SORTING_COMPLETE') {
      var d = event.data.data;
      Qualtrics.SurveyEngine.setEmbeddedData('sorting_result', JSON.stringify(d.groups));
      Qualtrics.SurveyEngine.setEmbeddedData('sorting_compact', d.compact);
      Qualtrics.SurveyEngine.setEmbeddedData('sorting_group_count', String(d.groupCount));
      if (d.mapping) Qualtrics.SurveyEngine.setEmbeddedData('sorting_mapping', d.mapping);
      that.clickNextButton();
    }
  });
});
```

Этот код:
- Слушает сообщения от iframe
- При получении результата сохраняет данные в Embedded Data
- Автоматически нажимает «Далее»

---

## 2. Формат данных

### `sorting_compact` (строка)

Формат: `группа1|группа2|группа3`, где каждая группа — список ID через запятую.

Пример: `SMPC-01,SMPC-02,SMPC-05|SMPC-03,SMPC-04|SMPC-06,SMPC-07`

### `sorting_result` (JSON)

Массив групп, каждая группа — массив ID (реальные имена файлов):

```json
[["SMPC-01","SMPC-02","SMPC-05"],["SMPC-03","SMPC-04"],["SMPC-06","SMPC-07"]]
```

### `sorting_mapping` (строка)

Соответствие «Stimulus 01»–«27» → реальный ID. Участник видит Stimulus 01, 02… по порядку, но за каждым скрыт случайный SMPC-xx. Формат: `1:SMPC-15,2:SMPC-03,3:SMPC-22,...` — для проверки и анализа.

---

## 3. Важно про iframe и postMessage

- **Same-origin**: Если страница на другом домене (Vercel), postMessage работает — это стандартный способ обмена данными между iframe и родителем.
- **event.origin**: В продакшене можно проверять `if (event.origin === 'https://ваш-проект.vercel.app')` для безопасности.
- **Qualtrics**: Убедитесь, что в настройках аккаунта включены **Allow JavaScript** и **Allow All HTML Markup**.

---

## 4. Тестирование без Qualtrics

Откройте страницу напрямую в браузере. При нажатии «Done» данные выводятся в консоль (F12 → Console). В iframe внутри Qualtrics данные уйдут в родительское окно.
