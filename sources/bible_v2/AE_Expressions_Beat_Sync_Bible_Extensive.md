# 🎛️ AE Expressions — Beat Sync Bible
> Всемогущая методичка. Рвёт все туторы. Анимирует всё под бит.

---

## 📋 ОГЛАВЛЕНИЕ

- [[#🔊 АУДИО — ОСНОВА ВСЕГО]]
- [[#🎚️ АМПЛИТУДА — БАЗОВЫЕ ШАБЛОНЫ]]
- [[#📐 SCALE — МАСШТАБ]]
- [[#🔄 ROTATION — ВРАЩЕНИЕ]]
- [[#📍 POSITION — ПОЗИЦИЯ]]
- [[#🔢 VALUE DIAL — КРУТИЛКА / ЧИСЛОВОЕ ЗНАЧЕНИЕ]]
- [[#🎨 OPACITY — ПРОЗРАЧНОСТЬ]]
- [[#📏 STROKE WIDTH — ТОЛЩИНА ОБВОДКИ]]
- [[#🌈 COLOR — ЦВЕТ]]
- [[#🎭 MULTI-PROPERTY — НЕСКОЛЬКО СВОЙСТВ СРАЗУ]]
- [[#🏎️ EASING — СМЯГЧЕНИЯ]]
- [[#🔁 LOOP & REPEAT — ЦИКЛЫ]]
- [[#⚡ WIGGLE + BEAT — ВИГЛ ПОД БИТ]]
- [[#🎯 THRESHOLDS — ПОРОГОВЫЕ ЗНАЧЕНИЯ]]
- [[#📦 UTILS — ПОЛЕЗНЫЕ ФУНКЦИИ]]
- [[#🚀 FULL RIG — ГОТОВЫЕ РИГИ]]
- [[#🌊 SMOOTH MOTION — ПЛАВНОЕ ДВИЖЕНИЕ]]
- [[#🎲 RANDOM MOTION — РАНДОМНОЕ ДВИЖЕНИЕ]]
- [[#📡 INTERPOLATION — ИНТЕРПОЛЯЦИЯ МЕЖДУ ТОЧКАМИ]]
- [[#🔀 PROCEDURAL PATHS — ПРОЦЕДУРНЫЕ ТРАЕКТОРИИ]]
- [[#🧲 FOLLOW & INERTIA — ИНЕРЦИЯ И СЛЕДОВАНИЕ]]
- [[#🎛️ EXPRESSION CONTROLS — УПРАВЛЕНИЕ ЧЕРЕЗ UI]]
- [[#🔗 LINKING — СВЯЗЬ МЕЖДУ СЛОЯМИ]]
- [[#✍️ TEXT — РАБОТА С ТЕКСТОМ]]
- [[#🖼️ SHAPE LAYERS — ШЕЙП-СЛОИ]]
- [[#🎬 TIME — РАБОТА СО ВРЕМЕНЕМ]]
- [[#📷 CAMERA — КАМЕРА]]
- [[#💡 LIGHTS — СВЕТ]]
- [[#🌀 3D — ТРЁХМЕРНОЕ ПРОСТРАНСТВО]]
- [[#🔢 COUNTERS & TIMERS — СЧЁТЧИКИ]]
- [[#🎨 EFFECTS — КОНКРЕТНЫЕ ЭФФЕКТЫ]]
- [[#📐 MASKS & TRIM PATHS — МАСКИ И ОБРЕЗКА]]
- [[#🧮 MATH PATTERNS — МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ]]
- [[#🏗️ MASTER RIG v2 — PRODUCTION FULL RIG]]
	- [[#🎵 FREQUENCY BANDS — ЧАСТОТНЫЕ ДИАПАЗОНЫ]]
- [[#👥 CROWD RIG — ТОЛПЫ И МАССИВЫ]]
- [[#⚓ ANCHOR POINT — ТОЧКА ТРАНСФОРМАЦИИ]]
- [[#🎞️ COMP MARKERS — МАРКЕРЫ КОМПА]]
- [[#🌊 ADVANCED WIGGLE — ПРОДВИНУТЫЙ ВИГЛ]]
- [[#🎨 GRADIENT & COLOR ADVANCED — ЦВЕТ ПРОДВИНУТЫЙ]]
- [[#🪆 PARENTING & NULL TRICKS — НУЛЛЫ И ПЭРЕНТИНГ]]
- [[#💥 VFX SNIPPETS — ГОТОВЫЕ VFX СНИППЕТЫ]]
- [[#🔌 EXPRESSION TO EXPRESSION — ЦЕПОЧКИ]]
- [[#📊 DATA DRIVEN — ДАННЫЕ В АНИМАЦИЮ]]
- [[#🏃 MOTION DESIGN PATTERNS — ПАТТЕРНЫ MOTION]]
- [[#⚠️ TROUBLESHOOTING]]

---

# 📚 QUICK START — КАК ЧИТАТЬ EXPRESSIONS

---

## 🎯 Универсальная формула

Почти любой expression состоит из трёх частей:

```javascript
INPUT
↓
PROCESS
↓
OUTPUT
```

Пример:

```javascript
amp = audioLayer.effect("Both Channels")("Slider");

freq = ease(amp,0,20,1,10);

Math.sin(time*freq)*100;
```

Где:

```javascript
amp
```

➡ входные данные

```javascript
ease(...)
```

➡ обработка

```javascript
Math.sin(...)
```

➡ результат

---

## 🏎️ ease()

Плавное преобразование диапазона.

```javascript
ease(input, inMin, inMax, outMin, outMax);
```

Пример:

```javascript
ease(amp,0,20,100,200);
```

|Параметр|Значение|
|---|---|
|amp|что контролирует|
|0|минимум входа|
|20|максимум входа|
|100|минимум выхода|
|200|максимум выхода|

---

## 📈 linear()

То же самое, но без плавности.

```javascript
linear(amp,0,20,100,200);
```

Используй когда нужен жёсткий отклик.

---

## 🟢 easeIn()

Мягкий старт.

```javascript
easeIn(amp,0,20,100,200);
```

Подходит для:

- появления
    
- acceleration
    
- kiirendus
    
- 加速
    

---

## 🔴 easeOut()

Мягкая остановка.

```javascript
easeOut(amp,0,20,100,200);
```

Подходит для:

- затухания
    
- инерции
    
- aeglustus
    
- 減速
    

---

## 🌊 Math.sin()

Процедурное колебание.

```javascript
Math.sin(time*freq)*amp;
```

|Параметр|Значение|
|---|---|
|time|время|
|freq|скорость|
|amp|размах|

Пример:

```javascript
Math.sin(time*2)*100;
```

Диапазон:

```text
-100 ... +100
```

---

## 📳 wiggle()

Случайное движение.

```javascript
wiggle(freq,amp);
```

Пример:

```javascript
wiggle(5,50);
```

|Параметр|Значение|
|---|---|
|5|раз в секунду|
|50|максимальное отклонение|

---

## 🔗 Ease → Wiggle

Управляем силой wiggle через музыку.

```javascript
amount = ease(amp,0,20,0,100);

wiggle(5,amount);
```

---

## 🔗 Ease → Sin

Управляем скоростью колебания.

```javascript
freq = ease(amp,0,20,1,10);

Math.sin(time*freq)*100;
```

---

## 🔗 Ease → Rotation

Rotation ждёт число.

```javascript
ease(amp,0,20,0,45);
```

Работает сразу.

---

## 🔗 Ease → Position

Position ждёт массив.

Неправильно:

```javascript
ease(amp,0,20,0,45);
```

Правильно:

```javascript
offset = ease(amp,0,20,0,45);

[
 value[0],
 value[1]-offset
];
```

---

## 📦 Типы данных

### Одно число

```javascript
50
```

Используют:

- Rotation
    
- Opacity
    
- Slider
    

---

### Два числа

```javascript
[100,100]
```

Используют:

- Scale 2D
    
- Position 2D
    

---

### Три числа

```javascript
[100,100,100]
```

Используют:

- Scale 3D
    
- Position 3D
    

---

### Цвет

```javascript
[1,0,0,1]
```

Используют:

- Color
    

---

## 🚨 Если появилась ошибка

Проверь:

```text
□ Есть слой?
□ Есть эффект?
□ Правильное имя?
□ Число или массив?
□ 2D или 3D?
□ Не забыл [ ] ?
```

95% всех ошибок находятся здесь.


---
## 🔊 АУДИО — ОСНОВА ВСЕГО

### Базовая установка (делай первым делом всегда)

```javascript
// На нужном слое -> Expression -> любое свойство
// Сначала создай аудио-амплитуду:
// Анимация -> Keyframe Assistant -> Convert Audio to Keyframes
// Получишь слой [Audio Amplitude] с тремя каналами
```

### Ссылка на аудио-слой — три способа

```javascript
// Способ 1: по имени (САМЫЙ НАДЁЖНЫЙ)
audioLayer = thisComp.layer("Audio Amplitude");
both = audioLayer.effect("Both Channels")("Slider");

// Способ 2: оба канала
audioLayer = thisComp.layer("Audio Amplitude");
left  = audioLayer.effect("Left Channel")("Slider");
right = audioLayer.effect("Right Channel")("Slider");
both  = audioLayer.effect("Both Channels")("Slider");

// Способ 3: массив значений (vals — классика)
audioLayer = thisComp.layer("Audio Amplitude");
vals = [
  audioLayer.effect("Left Channel")("Slider").value,
  audioLayer.effect("Right Channel")("Slider").value,
  audioLayer.effect("Both Channels")("Slider").value
];
// vals[0] = left, vals[1] = right, vals[2] = both
```

### Усреднение каналов вручную

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
avg = (L + R) / 2;
// Используй avg вместо both — чуть стабильнее на моно-контенте
```

---

## 🎚️ АМПЛИТУДА — БАЗОВЫЕ ШАБЛОНЫ

### Сырой сигнал (без обработки — жёсткий отклик)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp;
```

### Умноженный сигнал (усиление)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp * 3;
// Множитель 1..10+ — подбирай под трек
```

### Clamp — обрезка диапазона

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
clamp(amp * 5, 0, 100);
// clamp(значение, мин, макс) — никогда не выйдет за рамки
```

### linear() — линейный маппинг амплитуды в любой диапазон

```javascript
// linear(t, tMin, tMax, valMin, valMax)
// t       — входное значение (амплитуда)
// tMin    — минимум входа (обычно 0)
// tMax    — максимум входа (подбирай под трек: 5..30)
// valMin  — что выдать при тишине
// valMax  — что выдать при максимуме

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
linear(amp, 0, 15, 100, 200);
// При тишине -> 100, при орущем басе -> 200
```

### ease() — то же но с плавными краями 

```javascript
// ease(t, tMin, tMax, valMin, valMax)
// Разница от linear: замедление на краях — выглядит органичнее

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 15, 100, 200);
// Плавнее чем linear, но чуть медленнее реагирует на атаку
```

### easeIn() / easeOut() — ассиметричное смягчение

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

// Плавный вход, резкий выход (атака мягкая):
easeIn(amp, 0, 15, 100, 200);

// Резкий вход, плавный выход (атака жёсткая, затухание мягкое):
easeOut(amp, 0, 15, 100, 200);
```

```javascript
ease(
 amp,   // чем управляем
 0,     // нижняя граница входа
 15,    // верхняя граница входа
 100,   // что выдать на минимуме
 200    // что выдать на максимуме
);
```

---

## 📐 SCALE — МАСШТАБ

> ⚠️ Scale в AE — это **массив** `[x, y]` или `[x, y, z]`. Не забывай!

### Scale — линейный отклик (жёсткий бит)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = linear(amp, 0, 20, 100, 150);
[s, s];
// Оба оси одинаково. При тишине 100%, при ударе 150%
```

### Scale — смягчённый

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 150);
[s, s];
```

### Scale — разные оси (X и Y независимо)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
sx = ease(amp, 0, 20, 80, 130);   // X сжимается сильнее
sy = ease(amp, 0, 20, 100, 115);  // Y чуть меньше
[sx, sy];
// Даёт эффект "сквош-страрч" под бит
```

### Scale — squash & stretch под бит (классика cartoon)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// При ударе: Y сжимается, X растягивается
sy = ease(amp, 0, 20, 100, 70);   // вертикаль уменьшается
sx = ease(amp, 0, 20, 100, 140);  // горизонталь растёт
[sx, sy];
```

### Scale — 3D слой

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 150);
[s, s, s];  // три оси: X, Y, Z
```

### Scale — от нуля до нужного значения (появление)

```javascript
// Полезно для intro-эффектов
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 25, 0, 100);
[s, s];
// Объект появляется только когда есть звук
```

### Scale — с offset (базовый размер + добавка от бита)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
base = 100;
boost = amp * 3;
s = base + boost;
[s, s];
```

### Scale — левый и правый канал на разные оси

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
sx = ease(L, 0, 20, 100, 150);
sy = ease(R, 0, 20, 100, 150);
[sx, sy];
// Стерео-реакция: каждая ось на свой канал
```

---

## 🔄 ROTATION — ВРАЩЕНИЕ

### Rotation — простой поворот под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 45);
// От 0 до 45 градусов под удар
```

### Rotation — смягчённый отклик

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, -15, 15);
// Качается туда-сюда от -15 до +15 под громкость
```

### Rotation — накопительное вращение (спиннер)

```javascript
// Чем громче — тем быстрее крутится
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
speed = ease(amp, 0, 20, 0, 360); // скорость в градусах в секунду
speed * time;
// Объект постоянно крутится, ускоряясь под бит
```

### Rotation — пружинящий отклик (bounce after beat)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
base = ease(amp, 0, 20, 0, 30);
// Добавляем mini-wiggle пропорционально амплитуде
wobble = wiggle(8, amp * 1.5);
base + wobble;
```

r### Rotation — маятник на ритме

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
freq = ease(amp, 0, 20, 1, 6);    // частота качания
decA = ease(amp, 0, 20, 0, 25);   // амплитуда качания
Math.sin(time * freq * Math.PI * 2) * decA;
```

---

## 📍 POSITION — ПОЗИЦИЯ

> ⚠️ Position — это всегда массив `[x, y]`!

### Position Y — прыжок вверх под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
offset = ease(amp, 0, 20, 0, -80);  // отрицательный Y = вверх
[value[0], value[1] + offset];
// value — оригинальная позиция слоя (не трогает кейфреймы!)
```

### Position Y — прыжок вниз (отдача)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
offset = ease(amp, 0, 20, 0, 60);   // положительный Y = вниз
[value[0], value[1] + offset];
```

### Position X — горизонтальный отклик

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
offset = ease(amp, 0, 20, 0, 40);
[value[0] + offset, value[1]];
```

### Position XY — оба оси вместе

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ox = ease(amp, 0, 20, 0, 30);
oy = ease(amp, 0, 20, 0, -50);
[value[0] + ox, value[1] + oy];
```

### Position — стерео-разброс (L/R каналы)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
ox = ease(R - L, -20, 20, -50, 50);  // дрейф по X по стерео-балансу
[value[0] + ox, value[1]];
```

### Position — вибрация (shake) под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 15);
freq = 20;  // частота шейка в Hz
ox = Math.sin(time * freq * 6.28) * shakeAmt;
oy = Math.cos(time * freq * 6.28 * 0.7) * shakeAmt;
[value[0] + ox, value[1] + oy];
```

### Position — орбита вокруг центра под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
radius = ease(amp, 0, 20, 20, 120);
speed = 2;  // оборотов в секунду
cx = thisComp.width / 2;
cy = thisComp.height / 2;
[cx + Math.cos(time * speed * Math.PI * 2) * radius,
 cy + Math.sin(time * speed * Math.PI * 2) * radius];
```

### Position — прыжок с возвратом (punchback)

```javascript
// Позиция прыгает вверх на удар, сразу падает обратно
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = -amp * 4;  // прямой быстрый отклик без смягчения
[value[0], value[1] + oy];
// Нет ease — резче реагирует. Подходит для ударных
```
### Position UP + Shake

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

jumpY = -amp * 4;

shakeAmt = ease(amp, 18, 26, 0, 10);
shakeFreq = 5;

shakeX = Math.sin(time * shakeFreq * Math.PI * 2) * shakeAmt;
shakeY = Math.cos(time * shakeFreq * Math.PI * 2 * 0.7) * shakeAmt;

[
    value[0] + shakeX,
    value[1] + jumpY + shakeY
];
```
### X - ПАНЧ + Shake

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

shakeAmt = ease(amp, 18, 26, 0, 10);

shakeX = Math.sin(time * 5 * 6.28) * shakeAmt;
shakeY = Math.cos(time * 5 * 6.28 * 0.7) * shakeAmt;

[
    value[0] + shakeX + amp * 4,
    value[1] + shakeY
];
```

### Случайный удар влево-вправо

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

seedRandom(
Math.floor(time*10),
true
);

jumpX =
random(-1,1)
*
amp
*
4;

[
    value[0] + jumpX,
    value[1]
];
```


### Случайный удар влево-вправо (Ease Amplitude)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

// Смягчаем аудио-сигнал
amp = ease(amp, 0, 30, 0, 30);

// Новое случайное направление 2 раза в секунду
seedRandom(Math.floor(time*2), true);

// Случайный толчок по X
jumpX = random(-1,1) * amp * 2;

[
    value[0] + jumpX,
    value[1]
];
```
### Случайный удар влево-вправо (Ease Punch)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

jumpStrength = ease(amp, 18, 26, 0, 20); // amp 18→0px, amp 26→20px

seedRandom(Math.floor(time*2), true);

jumpX = random(-1,1) * jumpStrength;

[value[0] + jumpX, value[1]];
```

---

### Крутилка 3: диапазон с offset (например blur от 0 до 40)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 40);
// Вешай на Gaussian Blur -> Blurriness
```

### Крутилка — Exposure / яркость под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 3);
// Вешай на Exposure -> Exposure
```

### Крутилка — Hue Rotate (сдвиг оттенка)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 180);
// Вешай на Hue/Saturation -> Master Hue
```

### Крутилка — числовое значение с пульсирующим offset

```javascript
// Базовое значение из кейфреймов + добавка от бита
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
boost = ease(amp, 0, 20, 0, 50);
value + boost;
// value = текущий кейфреймовый сдвиг, сверху добавляется амплитуда
```

---

## 🎨 OPACITY — ПРОЗРАЧНОСТЬ

### Opacity — пульс (100% -> dim под бит)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 30);
// При ударе слой темнеет до 30%
```

### Opacity — вспышка (0% -> 100% на удар)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
// Объект появляется только когда громко
```

### Opacity — мигание (strobe) под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Если amp > порога — показываем, иначе скрываем
amp > 10 ? 100 : 0;
```

### Opacity — плавное появление с порогом

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 5, 20, 0, 100);
// До 5 — невидим, от 5 до 20 — плавно проявляется
```

---

## 📏 STROKE WIDTH — ТОЛЩИНА ОБВОДКИ

```javascript
// Shape layer -> Contents -> Group -> Stroke -> Stroke Width
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 2, 20);
// От 2px до 20px под бит
```

---

## 🌈 COLOR — ЦВЕТ

### Color RGB под амплитуду

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
r = ease(amp, 0, 20, 0.1, 1.0);  // красный канал
g = ease(amp, 0, 20, 0.5, 0.0);  // зелёный убывает
b = 0.8;                           // синий фиксированный
a = 1.0;                           // альфа 100%
[r, g, b, a];
// Цвет меняется от тёмного к красному на ударе
```

### Color Hue shift через wiggle-подобный подход

```javascript
// Через Hue/Saturation effect, вешай на Master Hue
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// При ударе резкий сдвиг оттенка
ease(amp, 0, 20, 0, 120);
```

---

## 🎭 MULTI-PROPERTY — НЕСКОЛЬКО СВОЙСТВ СРАЗУ

### Rig через Slider Control (РЕКОМЕНДУЕТСЯ)

```javascript
// 1. Добавь на слой Effect -> Expression Controls -> Slider Control
// 2. Назови его "Beat"
// 3. На этот Slider вешай ОДНО выражение с амплитудой:

// [Slider Control "Beat" -> Slider]:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);

// 4. На Scale:
s = thisLayer.effect("Beat")("Slider");
mapped = ease(s, 0, 100, 100, 150);
[mapped, mapped];

// 5. На Rotation:
s = thisLayer.effect("Beat")("Slider");
ease(s, 0, 100, 0, 30);

// 6. На Position:
s = thisLayer.effect("Beat")("Slider");
oy = ease(s, 0, 100, 0, -60);
[value[0], value[1] + oy];
```

> **ПРОФИТ**: меняешь один Slider -> всё пересчитывается. Производительнее чем 10 отдельных ссылок на аудио-слой!

---

## 🏎️ EASING — СМЯГЧЕНИЯ

### Сравнение методов (выбирай правильный)

| Функция | Плавность | Скорость AE | Когда |
|---------|-----------|-------------|-------|
| `amp * multiplier` | Нет | ⚡ Быстро | Жёсткий пиксельный бит |
| `linear()` | Края нет | ⚡ Быстро | Точный маппинг |
| `ease()` | Оба края | ✅ Норм | Большинство случаев |
| `easeIn()` | Только вход | ✅ Норм | Мягкая атака |
| `easeOut()` | Только выход | ✅ Норм | Мягкое затухание |

### ease() — подробно

```javascript
// ease(t, tMin, tMax, value1, value2)
// t         — управляющее значение (амплитуда)
// tMin      — при этом t -> value1
// tMax      — при этом t -> value2
// Между: кривая Безье (hermite)

ease(amp, 0, 20, 100, 200);
// amp=0   -> 100
// amp=10  -> ~150 (с замедлением на краях)
// amp=20  -> 200
```

### Ручная кривая — cubic bezier через Math

```javascript
// Для максимальной органики — без функции ease()
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
t = clamp(amp / 20, 0, 1);  // нормализуем 0..1
// Cubic ease out: t * (2 - t)
curved = t * (2 - t);
// Маппим обратно:
100 + curved * 100;  // 100..200
```

### Затухание после удара (decay) — без кейфреймов!

```javascript
// Exponential decay — органичный отклик
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
decay = 0.85;  // 0.8..0.95 — скорость затухания
// НЕ РАБОТАЕТ напрямую в AE без кейфреймов без хака
// Используй вместо этого easeOut:
easeOut(amp, 0, 20, 100, 200);
// easeOut даёт органичное затухание после пика
```

---

## 🔁 LOOP & REPEAT — ЦИКЛЫ

### Базовый loop (pingpong, cycle)

```javascript
// На кейфреймированное свойство:
loopOut("cycle");    // повторяет последний кейфрейм цикла
loopOut("pingpong"); // туда-обратно
loopOut("offset");   // продолжает паттерн с нарастанием

loopIn("cycle");     // то же с начала
```

### Loop + Beat (пульс по времени)

```javascript
// Синусоидальный пульс независимо от аудио
freq = 2;   // удара в секунду
amp  = 50;  // диапазон
Math.sin(time * freq * Math.PI * 2) * amp;
```

### Loop с аудио-модуляцией скорости

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseFreq = 1;
modFreq  = ease(amp, 0, 20, 1, 4);  // ускоряется на ударе
range    = 30;
Math.sin(time * modFreq * Math.PI * 2) * range;
```

---

## ⚡ WIGGLE + BEAT — ВИГЛ ПОД БИТ

### wiggle() базовый

```javascript
// wiggle(frequency, amplitude, octaves, amp_mult, t)
wiggle(5, 20);  // 5 раз в секунду, диапазон 20px
```

### Wiggle с амплитудой от бита (КЛАССИКА)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 40);  // диапазон вигла от 0 до 40
wiggle(8, wAmp);
// При тишине — стоит. При ударе — трясётся
```

### Wiggle для Position

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 30);
w = wiggle(10, wAmp);
// Добавляем к оригинальной позиции:
[value[0] + w[0], value[1] + w[1]];
```

### Wiggle только по одной оси

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 25);
// Только по X:
[value[0] + wiggle(8, wAmp)[0], value[1]];
// Только по Y:
[value[0], value[1] + wiggle(8, wAmp)[1]];
```

### Wiggle для Rotation под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 15);
wiggle(6, wAmp);
// Ротация трясётся под бит
```

### Wiggle с seed (разные объекты не синхронно)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 30);
seedRandom(42, true);  // 42 = любое число, true = хронологически
wiggle(8, wAmp);
// Каждый объект с разным seed двигается по-своему
```

---

## 🎯 THRESHOLDS — ПОРОГОВЫЕ ЗНАЧЕНИЯ

### Бинарный триггер (вкл/выкл на ударе)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 12;  // порог срабатывания
amp > threshold ? 100 : 0;
// Вешай на Opacity: мигает строго на удар
```

### Два порога (тихо / средне / громко)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
if (amp < 5) {
  0;           // тихо — ноль
} else if (amp < 15) {
  50;          // средне — 50
} else {
  100;         // громко — 100
}
```

### Soft threshold — плавное включение от порога

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 8;
if (amp < threshold) {
  0;
} else {
  ease(amp, threshold, 25, 0, 100);
}
```

### Детектор удара — только первый импульс (peak hold)

```javascript
// Нет нативного peak-detector без кейфреймов
// Лучший workaround: низкий ease с коротким диапазоном
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 10, 20, 0, 100);  // реагирует только на пики выше 10
```

---

## 📦 UTILS — ПОЛЕЗНЫЕ ФУНКЦИИ

### Нормализация 0..1

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
maxAmp = 25;  // максимальная амплитуда твоего трека
t = clamp(amp / maxAmp, 0, 1);
// t теперь 0..1 — используй как угодно
t * 360;  // -> hue 0..360
t * 100;  // -> opacity 0..100
```

### Ссылка на другой слой (не аудио)

```javascript
// Берёт Scale из другого слоя
ref = thisComp.layer("Master Control");
s = ref.transform.scale[0];
s * 0.5;  // Half of master's scale
```

### Текущее время как входной параметр

```javascript
// Для синусоидальных анимаций без аудио:
freq = 1.5;  // Гц
range = 50;
Math.sin(time * freq * Math.PI * 2) * range + 100;
```

### Компенсация parent transform

```javascript
// Если слой в parent-null и ты не хочешь двойного умножения
// Вешай на child-слой:
fromCompToLocal(toComp([0, 0, 0]));
```

### Случайное значение привязанное к слою

```javascript
seedRandom(index, true);  // index = номер слоя, уникален
random(0, 100);           // уникальный случайный для каждого слоя
```

### time remapping под бит (ускорение видео)

```javascript
// На слой с видео -> Time Remap:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
speedMult = ease(amp, 0, 20, 0.5, 3.0);  // от 0.5x до 3x скорости
// Интегрируем скорость для time remap:
// (Это сложнее — нужна апроксимация через delta)
value + (speedMult - 1) * thisComp.frameDuration;
```

---

## 🚀 FULL RIG — ГОТОВЫЕ РИГИ

### RIG 1: Полный бит-риг через Null (PRODUCTION READY)

```
Структура:
[Null "BEAT_MASTER"] <- сюда вешаем все expressions
  L_ [Shape/Text Layer] <- ссылается на Null

1. Создай Null -> назови "BEAT_MASTER"
2. Добавь Effect -> Expression Controls -> Slider Control, назови "Beat Raw"
3. Добавь Effect -> Expression Controls -> Slider Control, назови "Beat Smooth"
```

```javascript
// [Null "BEAT_MASTER"] -> Slider Control "Beat Raw" -> Slider:
audioLayer = thisComp.layer("Audio Amplitude");
audioLayer.effect("Both Channels")("Slider");

// [Null "BEAT_MASTER"] -> Slider Control "Beat Smooth" -> Slider:
raw = thisLayer.effect("Beat Raw")("Slider");
ease(raw, 0, 20, 0, 100);

// Теперь на любом дочернем слое -> Scale:
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
mapped = ease(s, 0, 100, 100, 160);
[mapped, mapped];

// На Rotation:
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
ease(s, 0, 100, 0, 20);

// На Position Y:
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
oy = ease(s, 0, 100, 0, -50);
[value[0], value[1] + oy];
```

### RIG 2: Equalizer-бар (один expression для высоты бара)

```javascript
// Shape Layer -> Contents -> Rectangle -> Rectangle Path -> Size
// Ставишь на размер Y каждого бара с разным seed

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Добавь случайный offset для каждого бара:
seedRandom(index * 13, true);  // разное для каждого слоя
rndOffset = random(-5, 5);
h = ease(amp + rndOffset, 0, 20, 10, 200);
[value[0], h];  // ширина фиксирована, высота — от бита
```

### RIG 3: Радиальный visualizer (позиция по кругу + scale)

```javascript
// На каждом слое-элементе вокруг центра:
// Position:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
seedRandom(index, true);
baseRadius = 200;
beatRadius = ease(amp, 0, 20, 0, 80);
radius = baseRadius + beatRadius;
angle = (index / totalLayers) * Math.PI * 2;  // totalLayers = кол-во слоёв
cx = thisComp.width / 2;
cy = thisComp.height / 2;
[cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius];

// Scale на тех же слоях:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 50, 150);
[s, s];
```

### RIG 4: Типографика — Scale + Opacity + Position вместе

```javascript
// Все три — на ОДНОМ текстовом слое

// Scale:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 95, 115);
[s, s];

// Opacity:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 70, 100);

// Position:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = ease(amp, 0, 20, 5, -10);
[value[0], value[1] + oy];
// Текст "дышит" — чуть поднимается и светлеет на удар
```

### RIG 5: Camera shake под бит

```javascript
// Camera -> Position (3D comp):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 25);
w = wiggle(15, shakeAmt);
[w[0], w[1], value[2]];  // Z не трогаем

// Camera -> Rotation X (roll):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 2);
wiggle(12, shakeAmt);
```

### RIG 6: Particle-like dots (много слоёв, каждый реагирует по-своему)

```javascript
// Scale — на каждой "точке":
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
seedRandom(index * 7, true);
delay = random(0, 0.1);  // случайная задержка (имитация)
delayedAmp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider").valueAtTime(time - delay);
s = ease(delayedAmp, 0, 20, 30, 120);
[s, s];
// Каждая точка реагирует с чуть разной задержкой
```

---

## 🌊 SMOOTH MOTION — ПЛАВНОЕ ДВИЖЕНИЕ

> Без кейфреймов. Всё живое, дышит, не дёргается. Математика — твой друг.

### Синус — базовое дыхание (туда-сюда)

```javascript
// Math.sin(time * speed * TAU) * amplitude + center
// TAU = Math.PI * 2 = полный оборот синуса
freq  = 1.0;   // циклов в секунду (1 = один качок в секунду)
amp   = 50;    // диапазон движения в пикселях
center = 0;    // центральная точка смещения
offset = Math.sin(time * freq * Math.PI * 2) * amp + center;
[value[0], value[1] + offset];
// Y качается туда-сюда плавно и бесконечно
```

### Косинус — то же но со сдвигом фазы на 90°

```javascript
// Косинус начинает с максимума, синус — с нуля
freq = 1.0;
amp  = 50;
offset = Math.cos(time * freq * Math.PI * 2) * amp;
[value[0] + offset, value[1]];
// Используй cos для X и sin для Y -> получишь орбиту (см. ниже)
```

### Орбита — круговое плавное движение

```javascript
freq = 0.5;    // оборотов в секунду
radius = 80;   // радиус орбиты
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
angle = time * freq * Math.PI * 2;
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
// Идеальный круг. Медленно — красиво.
```

### Эллипс — разные радиусы по X и Y

```javascript
freq = 0.4;
rx = 150;  // радиус по X
ry = 60;   // радиус по Y
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
angle = time * freq * Math.PI * 2;
[cx + Math.cos(angle) * rx,
 cy + Math.sin(angle) * ry];
```

### Фигура Лиссажу (восьмёрка, клевер, etc.)

```javascript
// Разные частоты по X и Y = фигуры Лиссажу
freqX = 2.0;  // частота по X
freqY = 3.0;  // частота по Y (отношение = форма фигуры)
rx = 120;
ry = 120;
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
phaseX = 0;
phaseY = Math.PI / 4;  // фаза сдвига Y — меняет "наклон" фигуры
[cx + Math.cos(time * freqX * Math.PI * 2 + phaseX) * rx,
 cy + Math.sin(time * freqY * Math.PI * 2 + phaseY) * ry];
// freqX:freqY = 1:1 -> круг
// freqX:freqY = 1:2 -> восьмёрка
// freqX:freqY = 2:3 -> трилистник
// freqX:freqY = 3:4 -> "бант"
```

### Синус + бит = дыхание с акцентом

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

baseFreq  = 0.8;                               // базовая частота дыхания
baseAmp   = 30;                                // базовый диапазон
beatBoost = ease(amp, 0, 20, 0, 80);           // добавка на удар

offset = Math.sin(time * baseFreq * Math.PI * 2) * baseAmp + beatBoost;
[value[0], value[1] + offset];
// Слой плавно дышит сам по себе, а на удар — резкий импульс сверху
```

### Двойной синус — непредсказуемое дыхание

```javascript
// Складываем два синуса с некратными частотами -> никогда не повторяется
freq1 = 0.7;   amp1 = 30;
freq2 = 1.3;   amp2 = 15;
offset = Math.sin(time * freq1 * Math.PI * 2) * amp1
       + Math.sin(time * freq2 * Math.PI * 2) * amp2;
[value[0], value[1] + offset];
// Органично, никогда не зацикливается точно. Как живое.
```

### Тройной синус — максимально органично

```javascript
freq1 = 0.5;  amp1 = 40;
freq2 = 1.1;  amp2 = 20;
freq3 = 2.3;  amp3 = 8;
offset = Math.sin(time * freq1 * Math.PI * 2) * amp1
       + Math.sin(time * freq2 * Math.PI * 2) * amp2
       + Math.sin(time * freq3 * Math.PI * 2) * amp3;
[value[0], value[1] + offset];
// 3 слоя = очень живое. Больше 3 — уже не слышна разница.
```

### Синус для Rotation — качание маятника

```javascript
freq = 0.6;   // медленный качок
amp  = 20;    // максимальный угол в градусах
Math.sin(time * freq * Math.PI * 2) * amp;
```

### Синус для Scale — пульсирование

```javascript
freq = 1.2;
base = 100;
range = 15;
s = base + Math.sin(time * freq * Math.PI * 2) * range;
[s, s];
// Объект постоянно пульсирует между 85% и 115%
```

### Плавная остановка в точке — smoothstep вручную

```javascript
// smoothstep(edge0, edge1, x) — аналог ease() для произвольных значений
function smoothstep(e0, e1, x) {
  t = clamp((x - e0) / (e1 - e0), 0, 1);
  return t * t * (3 - 2 * t);
}
// Пример: анимация от 0 до 1 за первые 2 секунды
t = smoothstep(0, 2, time);
t * 100;  // 0..100 с плавным стартом и плавной остановкой
```

### Затухающее колебание (decaying oscillation) — bounce без кейфреймов

```javascript
// Имитация пружины: амплитуда убывает со временем
startTime = 1.0;   // когда начинается колебание (в секундах)
freq      = 6.0;   // частота колебания
decay     = 4.0;   // скорость затухания (больше = быстрее)
initAmp   = 60;    // начальная амплитуда

t = time - startTime;
if (t < 0) {
  value[1];
} else {
  damped = initAmp * Math.exp(-decay * t) * Math.sin(freq * Math.PI * 2 * t);
  value[1] + damped;
}
// Используй в массиве: [value[0], выражение_выше]
```

### Затухающее колебание привязанное к биту

```javascript
// Каждый удар запускает колебание заново
// Нужна кейфреймовая "метка удара" на отдельном Slider
// Или: valueAtTime — тяжело. Лучший workaround — easeOut + wiggle:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
bounce = easeOut(amp, 0, 20, 0, 50);
// easeOut даёт быстрый подъём и медленное затухание = имитация bounce
[value[0], value[1] - bounce];
```

---

## 🎲 RANDOM MOTION — РАНДОМНОЕ ДВИЖЕНИЕ

> wiggle() — это хорошо. Но это не единственный способ.

### wiggle() — шпаргалка по параметрам

```javascript
// wiggle(freq, amp, octaves, amp_mult, t)
//   freq     — колебаний в секунду
//   amp      — максимальное отклонение
//   octaves  — слоёв шума (1..4, default=1, больше = детальнее)
//   amp_mult — как убывает амплитуда от октавы к октаве (0..1, default=0.5)
//   t        — время (default=time, можно подать своё)

wiggle(3, 30);              // базовый: 3 раза/сек, ±30px
wiggle(3, 30, 3, 0.5);     // 3 октавы — более детальный шум
wiggle(10, 5);              // быстрый мелкий дрожащий шум
wiggle(0.3, 100);           // редкие большие дрейфы
```

### Плавный рандомный дрейф (slow drift) — НЕ дёрганый

```javascript
// Секрет: очень низкая freq + большая amp
wiggle(0.2, 80);
// 0.2 раза в секунду — очень медленно меняет направление
// Выглядит как органичный float, не как дрожание
```

### Рандомное движение только по X или Y

```javascript
// Только X:
w = wiggle(1, 40);
[value[0] + w[0], value[1]];

// Только Y:
w = wiggle(1, 40);
[value[0], value[1] + w[1]];

// Разные параметры на каждую ось:
wx = wiggle(0.5, 60)[0];   // медленно по X
wy = wiggle(2.0, 20)[1];   // быстро по Y
[value[0] + wx, value[1] + wy];
```

### Рандомное движение с разными seed (толпа объектов)

```javascript
// Каждый слой двигается по-своему, но с одинаковой "энергией"
// seedRandom(seed, timeless) — timeless=true -> seed не меняется со временем
// timeless=false -> seed сам по себе меняется (не то что нам нужно)

// Для уникального wiggle на каждом слое:
// (wiggle всегда использует index как часть seed — они уже разные)
// Но если хочешь контролировать:
mySeed = index * 37 + 5;  // любая формула от index
seedRandom(mySeed, true);  // timeless=true чтобы не сбивало каждый кадр

// Теперь wiggle будет разным, но воспроизводимым для этого слоя:
wiggle(1, 50);
```

### Рандомная скорость дрейфа — у каждого объекта своя

```javascript
seedRandom(index * 13, true);
myFreq = random(0.2, 1.5);   // каждый объект со своей частотой
myAmp  = random(20, 80);     // и своей амплитудой
w = wiggle(myFreq, myAmp);
[value[0] + w[0], value[1] + w[1]];
```

### Случайная задержка реакции (stagger) для толпы

```javascript
// Каждый слой реагирует на бит с разной задержкой — выглядит живо
seedRandom(index * 7, true);
lag = random(0, 0.3);  // задержка 0..0.3 секунды
audioLayer = thisComp.layer("Audio Amplitude");
delayedAmp = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - lag);
s = ease(delayedAmp, 0, 20, 100, 160);
[s, s];
```

### Step random — дискретные прыжки (не плавно, а ступеньками)

```javascript
// Значение меняется раз в N секунд — дискретный рандом
interval = 0.5;  // раз в полсекунды прыгает
stepTime  = Math.floor(time / interval) * interval;
seedRandom(stepTime * 1000 + index, true);
random(-50, 50);
// Резкие дискретные прыжки в рандомную точку
```

### Step random с плавным переходом между шагами (lerp)

```javascript
// Прыгает дискретно, но между значениями — линейная интерполяция
interval = 0.5;
t        = time / interval;
tFloor   = Math.floor(t);
tFrac    = t - tFloor;  // 0..1 внутри текущего интервала

seedRandom(tFloor * 100 + index, true);
v1 = random(-50, 50);
seedRandom((tFloor + 1) * 100 + index, true);
v2 = random(-50, 50);

// Линейная интерполяция между v1 и v2:
v1 + (v2 - v1) * tFrac;
// Плавно едет от одной рандомной точки к следующей
```

### Step random — SMOOTH версия (ease между шагами, не linear)

```javascript
interval = 0.8;
t        = time / interval;
tFloor   = Math.floor(t);
tFrac    = t - tFloor;

// Smoothstep вместо linear:
st = tFrac * tFrac * (3 - 2 * tFrac);

seedRandom(tFloor * 100 + index, true);
v1 = random(-60, 60);
seedRandom((tFloor + 1) * 100 + index, true);
v2 = random(-60, 60);

v1 + (v2 - v1) * st;
// Выглядит как ease кейфреймы, только без кейфреймов и в рандоме
```

### Рандомное направление движения (random walk) — накопительный дрейф

```javascript
// Объект медленно бредёт в случайном направлении
// Простая версия через медленный wiggle:
speed = 30;  // px/sec максимум
w = wiggle(0.15, speed);
// Интегрируем скорость в позицию:
// (AE не умеет интегрировать напрямую — используем time как proxy)
[value[0] + w[0] * time * 0.1,
 value[1] + w[1] * time * 0.1];
// Примерная симуляция. Для точного random walk нужны кейфреймы.
```

### Рандомный scale для каждого объекта в массиве

```javascript
// Фиксированный рандомный scale — у каждого слоя свой, но не меняется
seedRandom(index * 23, true);
s = random(60, 140);  // каждый объект от 60% до 140%
[s, s];
// Хорошо для толп, частиц, фоновых элементов
```

### Рандомный offset позиции — сдвиг от якоря

```javascript
seedRandom(index * 17, true);
ox = random(-100, 100);  // случайный сдвиг по X
oy = random(-100, 100);  // случайный сдвиг по Y
[value[0] + ox, value[1] + oy];
// Разбрасывает объекты вокруг их оригинальной позиции
```

### Рандомная фаза синуса — толпа дышит вразнобой

```javascript
seedRandom(index * 11, true);
phase = random(0, Math.PI * 2);  // случайная начальная фаза
freq  = 0.8;
amp   = 30;
offset = Math.sin(time * freq * Math.PI * 2 + phase) * amp;
[value[0], value[1] + offset];
// Все качаются с одной частотой, но не синхронно — как водоросли
```

### Рандомная частота + фаза — полный хаос с порядком

```javascript
seedRandom(index * 31, true);
freq  = random(0.3, 1.5);
phase = random(0, Math.PI * 2);
amp   = random(15, 50);
offset = Math.sin(time * freq * Math.PI * 2 + phase) * amp;
[value[0], value[1] + offset];
// Каждый объект своя скорость, своя фаза, своя амплитуда
```

---

## 📡 INTERPOLATION — ИНТЕРПОЛЯЦИЯ МЕЖДУ ТОЧКАМИ

> Двигаться из А в Б плавно, без кейфреймов — это искусство.

### lerp() — линейная интерполяция (нет в AE нативно, но легко)

```javascript
// lerp(a, b, t) = a + (b - a) * t
// t: 0 = точка A, 1 = точка B, 0.5 = середина
function lerp(a, b, t) { return a + (b - a) * t; }

// Пример: позиция между двумя точками
t = clamp(time / 3, 0, 1);  // 3 секунды на переход
x = lerp(100, 900, t);
y = lerp(200, 600, t);
[x, y];
```

### Ease между двумя позициями (smoothstep lerp)

```javascript
function smoothstep(t) { return t * t * (3 - 2 * t); }
function lerpSmooth(a, b, t) { return a + (b - a) * smoothstep(clamp(t, 0, 1)); }

dur = 2.0;  // длительность перехода в секундах
t = time / dur;
x = lerpSmooth(100, 800, t);
y = lerpSmooth(500, 200, t);
[x, y];
```

### Интерполяция через массив точек (по очереди)

```javascript
// Объект проходит по точкам A -> B -> C -> D
points = [[100, 540], [500, 200], [900, 540], [500, 800]];
segDur = 1.5;  // секунд на каждый сегмент

totalTime = segDur * (points.length - 1);
t = clamp(time, 0, totalTime);
seg = Math.floor(t / segDur);
seg = Math.min(seg, points.length - 2);  // не выйти за массив
tSeg = (t - seg * segDur) / segDur;      // 0..1 внутри сегмента
st   = tSeg * tSeg * (3 - 2 * tSeg);    // smoothstep

A = points[seg];
B = points[seg + 1];
[A[0] + (B[0] - A[0]) * st,
 A[1] + (B[1] - A[1]) * st];
// Плавно едет по точкам. Можно добавить/изменить points[]
```

### Интерполяция по кругу замкнутому (points loop)

```javascript
points = [[100, 540], [500, 100], [900, 540], [500, 900]];
segDur = 1.0;
n = points.length;
t = time % (segDur * n);  // зацикливаем
seg = Math.floor(t / segDur);
tSeg = (t - seg * segDur) / segDur;
st   = tSeg * tSeg * (3 - 2 * tSeg);

A = points[seg % n];
B = points[(seg + 1) % n];
[A[0] + (B[0] - A[0]) * st,
 A[1] + (B[1] - A[1]) * st];
// Бесконечный маршрут по точкам
```

### Интерполяция значений под бит (beat-triggered lerp)

```javascript
// Значение плавно едет к целевому, цель меняется под удар
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

target = ease(amp, 0, 20, 100, 200);  // цель зависит от бита
// "Расстояние" до цели — linear приближение:
// AE не умеет помнить предыдущий кадр без хаков.
// Используй easeOut как имитацию инерции:
easeOut(amp, 0, 20, 100, 200);
// easeOut = быстрый старт, медленный финиш = визуально похоже на lerp
```

---

## 🔀 PROCEDURAL PATHS — ПРОЦЕДУРНЫЕ ТРАЕКТОРИИ

### Спираль (расходящаяся)

```javascript
speed  = 1.0;   // оборотов в секунду
growth = 30;    // px добавляется к радиусу каждую секунду
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
angle  = time * speed * Math.PI * 2;
radius = time * growth;
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
```

### Спираль сходящаяся (к центру)

```javascript
speed    = 1.2;
maxRad   = 400;
duration = 5.0;   // секунд до центра
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
t  = clamp(time / duration, 0, 1);
angle  = time * speed * Math.PI * 2;
radius = maxRad * (1 - t);
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
```

### Восьмёрка (lemniscate Bernoulli)

```javascript
// Настоящая восьмёрка — формула Бернулли
speed = 0.5;
a     = 150;   // "размах" восьмёрки
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
angle = time * speed * Math.PI * 2;
scale_ = a / (1 + Math.sin(angle) * Math.sin(angle));
[cx + scale_ * Math.cos(angle),
 cy + scale_ * Math.sin(angle) * Math.cos(angle)];
```

### Зигзаг (линейный, туда-сюда)

```javascript
// Треугольная волна вместо синуса = острые пики
freq = 1.0;   // зигзагов в секунду
amp  = 100;
t    = time * freq;
// Треугольная волна: |2*(t - floor(t+0.5))|
tri  = Math.abs(2 * (t - Math.floor(t + 0.5)));
[value[0], value[1] + (tri * 2 - 1) * amp];
// Движется вверх-вниз острыми зигзагами
```

### Прямоугольная волна (step) — дискретные прыжки равномерно

```javascript
// Объект прыгает между двумя позициями ритмично
freq  = 2.0;  // переключений в секунду
posA  = -80;
posB  =  80;
t     = Math.floor(time * freq) % 2;  // 0 или 1, переключается
pos   = t === 0 ? posA : posB;
[value[0] + pos, value[1]];
```

### Пила (sawtooth) — линейный нарастающий сброс

```javascript
// Нарастает линейно, резко сбрасывается в ноль
freq = 0.5;   // циклов в секунду
amp  = 150;
t    = (time * freq) % 1;  // 0..1 пила
offset = t * amp * 2 - amp; // -amp..+amp
[value[0] + offset, value[1]];
```

### Bouncing ball — физика отскока без плагинов

```javascript
// Мяч падает вниз, отскакивает с затуханием
// Лучший способ — через кейфреймы + loopOut("pingpong") на Y
// Без кейфреймов — имитация через затухающий синус:
startTime = 0;
dur       = 1.2;   // период одного отскока
decayRate = 1.5;   // скорость затухания (выше = быстрее гасится)
gravity   = 200;   // "высота" первого отскока

t = time - startTime;
if (t < 0) {
  value[1];
} else {
  bounceAmp = gravity * Math.exp(-decayRate * t);
  bounce    = Math.abs(Math.sin(t / dur * Math.PI));
  value[1] + bounceAmp * bounce;  // вниз = + в AE
}
// Для Position вешай как: [value[0], выражение]
```

---

## 🧲 FOLLOW & INERTIA — ИНЕРЦИЯ И СЛЕДОВАНИЕ

> Один из самых крутых приёмов — объект не прыгает сразу, а "догоняет" цель.

### Инерция через valueAtTime (КЛАССИКА)

```javascript
// Берём значение свойства из прошлого — создаёт "задержку"
delay = 0.15;  // секунд отставания
thisLayer.transform.position.valueAtTime(time - delay);
// Вешать НА ТО ЖЕ СВОЙСТВО где уже есть кейфреймы!
// Слой будет повторять свою же траекторию с задержкой
```

### Инерция с масштабированием (сильнее тормозит)

```javascript
delay = 0.25;
v = thisLayer.transform.position.valueAtTime(time - delay);
// Интерполируем между текущим и задержанным:
t = 0.6;  // 0 = полная задержка, 1 = без задержки
cur = thisLayer.transform.position.valueAtTime(time);
[cur[0] + (v[0] - cur[0]) * (1 - t),
 cur[1] + (v[1] - cur[1]) * (1 - t)];
```

### Следование за другим слоем с инерцией

```javascript
// Слой B следует за слоем A с задержкой
delay = 0.2;
leader = thisComp.layer("Leader");
leader.transform.position.valueAtTime(time - delay);
// Слой-B плавно тянется за Лидером
```

### Следование с разной задержкой (цепочка)

```javascript
// У каждого слоя в цепочке — больше задержки
// Слой 1: delay=0 (лидер)
// Слой 2: delay=0.1
// Слой 3: delay=0.2
// и т.д.
// На каждом слое:
myDelay = (index - 1) * 0.08;  // index начинается с 1 в AE
leader  = thisComp.layer("Leader");
leader.transform.position.valueAtTime(time - myDelay);
// "Хвост" из объектов следует за лидером
```

### Инерция через loopOut + valueAtTime (хак для smooth)

```javascript
// Для очень плавного дрейфа позиции
// Работает если есть хотя бы 2 кейфрейма:
delay = 0.3;
value + (value - valueAtTime(time - delay)) * (-0.5);
// Тормозит и сглаживает движение по кейфреймам
```

### Пружина (spring) — объект тянется к целевой точке

```javascript
// Формула: простая имитация через sinusoidal decay
// targetX, targetY — куда тянемся
targetX = thisComp.width  / 2;
targetY = thisComp.height / 2;
freq    = 3.0;   // жёсткость пружины (выше = жёстче)
decay   = 2.0;   // затухание (выше = быстрее успокаивается)

t = time;
envelope = Math.exp(-decay * t);
springX  = targetX + (value[0] - targetX) * envelope * Math.cos(freq * Math.PI * 2 * t);
springY  = targetY + (value[1] - targetY) * envelope * Math.cos(freq * Math.PI * 2 * t);
[springX, springY];
// Объект притягивается к центру, колеблется и останавливается
```

---

## 🎛️ EXPRESSION CONTROLS — УПРАВЛЕНИЕ ЧЕРЕЗ UI

> Самый правильный подход — выносить все параметры в контролы. Не хардкодить.

### Полный набор контролов на Null-слой

```javascript
// Effect -> Expression Controls:
// Slider Control  -> "Freq"       (значение: 1.0)
// Slider Control  -> "Amplitude"  (значение: 50)
// Slider Control  -> "Decay"      (значение: 2.0)
// Slider Control  -> "Phase"      (значение: 0)
// Checkbox Control -> "Enable"    (вкл/выкл всего)
// Point Control   -> "Target XY"  (точка назначения)
// Color Control   -> "Beat Color" (цвет под бит)
// Angle Control   -> "Direction"  (угол движения)
```

### Использование контролов в expressions

```javascript
ctrl = thisComp.layer("CONTROLS");

freq  = ctrl.effect("Freq")("Slider");
amp   = ctrl.effect("Amplitude")("Slider");
phase = ctrl.effect("Phase")("Slider") * Math.PI / 180;  // в радианы

offset = Math.sin(time * freq * Math.PI * 2 + phase) * amp;
[value[0], value[1] + offset];
```

### Checkbox — вкл/выкл всего

```javascript
ctrl    = thisComp.layer("CONTROLS");
enabled = ctrl.effect("Enable")("Checkbox");

if (enabled) {
  audioLayer = thisComp.layer("Audio Amplitude");
  amp_ = audioLayer.effect("Both Channels")("Slider");
  s = ease(amp_, 0, 20, 100, 160);
  [s, s];
} else {
  value;  // вернуть оригинал без изменений
}
```

### Point Control как цель для движения

```javascript
ctrl   = thisComp.layer("CONTROLS");
target = ctrl.effect("Target XY")("Point");
// target = [x, y] в координатах компа

// Линейно едем к точке за 3 секунды:
t = clamp(time / 3, 0, 1);
st = t * t * (3 - 2 * t);  // smoothstep
[value[0] + (target[0] - value[0]) * st,
 value[1] + (target[1] - value[1]) * st];
```

### Angle Control для направления wiggle

```javascript
ctrl = thisComp.layer("CONTROLS");
dir  = ctrl.effect("Direction")("Angle") * Math.PI / 180;  // градусы -> радианы
amp_ = 60;
freq = 1.5;
dist = Math.sin(time * freq * Math.PI * 2) * amp_;

// Движение вдоль угла dir:
[value[0] + Math.cos(dir) * dist,
 value[1] + Math.sin(dir) * dist];
// Перетаскиваешь "Direction" -> меняешь ось качания
```

### Slider как множитель "глобальной энергии"

```javascript
// Один слайдер управляет интенсивностью ВСЕГО рига
ctrl   = thisComp.layer("CONTROLS");
energy = ctrl.effect("Energy")("Slider");  // 0..100

audioLayer = thisComp.layer("Audio Amplitude");
amp_ = audioLayer.effect("Both Channels")("Slider");
// Масштабируем ответ рига на energy:
s = ease(amp_, 0, 20, 100, 100 + energy);
[s, s];
// energy=0 -> нет реакции, energy=100 -> полная
```

---

## 🔗 LINKING — СВЯЗЬ МЕЖДУ СЛОЯМИ

> Один слой управляет другим. Никакой ручной анимации дважды.

### Зеркальная позиция (симметрия)

```javascript
// Слой B зеркалит позицию слоя A относительно центра
leader = thisComp.layer("Element_A");
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
posA = leader.transform.position;
[2 * cx - posA[0], posA[1]];  // зеркало по X
// [posA[0], 2 * cy - posA[1]];  // зеркало по Y
```

### Инверсия rotation

```javascript
// Слой B вращается в обратную сторону от слоя A
leader = thisComp.layer("Gear_A");
-leader.transform.rotation;
// Шестерня B вращается против шестерни A
```

### Синхронный scale с коэффициентом

```javascript
// Слой B = 70% от размера слоя A
leader = thisComp.layer("Master");
s = leader.transform.scale[0] * 0.7;
[s, s];
```

### Opacity одного зависит от position другого

```javascript
// Чем ближе слой к центру — тем более прозрачен
ref = thisComp.layer("MovingDot");
pos = ref.transform.position;
cx  = thisComp.width  / 2;
cy  = thisComp.height / 2;
dist = length(pos, [cx, cy]);  // length() — встроенная в AE
ease(dist, 0, 400, 0, 100);   // далеко = видно, близко = прозрачно
```

### Скорость другого слоя как входной параметр

```javascript
// Чем быстрее движется Leader — тем больше Scale у текущего
leader = thisComp.layer("Leader");
dt     = thisComp.frameDuration;
posNow  = leader.transform.position.valueAtTime(time);
posPrev = leader.transform.position.valueAtTime(time - dt);
// Скорость = расстояние / время:
vel = length(posNow, posPrev) / dt;
s = ease(vel, 0, 500, 100, 200);  // 500 px/sec = максимум
[s, s];
```

### Родитель-ребёнок через expression (без Parent пика)

```javascript
// Ребёнок следует за родителем, но с дополнительным сдвигом
parent_ = thisComp.layer("Parent_Null");
parentPos = parent_.transform.position;
localOffset = [50, -30];  // смещение от родителя
[parentPos[0] + localOffset[0],
 parentPos[1] + localOffset[1]];
```

---

## ✍️ TEXT — РАБОТА С ТЕКСТОМ

> Text expressions — отдельный мир. Source Text, Animator, per-character. Сила здесь огромная.

### Source Text — динамический счётчик кадров

```javascript
// На Text Layer -> Source Text:
"Frame: " + Math.floor(time * thisComp.frameRate);
```

### Source Text — таймер обратного отсчёта (MM:SS)

```javascript
totalSec = 60;  // с чего считаем
remaining = Math.max(0, totalSec - time);
mins = Math.floor(remaining / 60);
secs = Math.floor(remaining % 60);
// Форматирование с ведущим нулём:
mm = mins < 10 ? "0" + mins : "" + mins;
ss = secs < 10 ? "0" + secs : "" + secs;
mm + ":" + ss;
```

### Source Text — счётчик вверх с форматированием

```javascript
// Считает от 0 до maxVal за duration секунд
maxVal   = 1000;
duration = 3.0;
t = clamp(time / duration, 0, 1);
st = t * t * (3 - 2 * t);  // smoothstep — разгон и торможение
val = Math.round(st * maxVal);
// Добавим разделитель тысяч:
s = "" + val;
if (val >= 1000) {
  s = s.slice(0, -3) + " " + s.slice(-3);
}
s;
```

### Source Text — значение из Slider Control на экране

```javascript
// Показывает текущее значение слайдера как текст
ctrl = thisLayer.effect("My Slider")("Slider");
Math.round(ctrl) + "%";
```

### Source Text — Beat-счётчик (считает удары)

```javascript
// Нужен Checkbox Control "Beat Trigger" с кейфреймами 0/1 по ударам
// Или просто считаем по времени:
bpm    = 120;   // удары в минуту
beat   = Math.floor(time / (60 / bpm)) + 1;
"Beat " + beat;
```

### Source Text — случайные символы (glitch-эффект)

```javascript
// Текст рандомно меняет символы — матрица/глитч
chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%";
len     = 8;   // длина строки
fps     = thisComp.frameRate;
frame   = Math.floor(time * fps);  // меняется каждый кадр
result  = "";
for (i = 0; i < len; i++) {
  seedRandom(frame * len + i, true);
  idx = Math.floor(random(0, chars.length));
  result += chars[idx];
}
result;
```

### Source Text — глитч с частичным разоблачением финального слова

```javascript
// Начинает как мусор, постепенно "разоблачает" нужное слово
target  = "OBSIDIAN";
chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$";
dur     = 2.0;   // за сколько секунд полностью открывается
t       = clamp(time / dur, 0, 1);
revealed = Math.round(t * target.length);  // сколько букв уже "настоящие"
fps     = thisComp.frameRate;
frame   = Math.floor(time * fps);
result  = "";
for (i = 0; i < target.length; i++) {
  if (i < revealed) {
    result += target[i];
  } else {
    seedRandom(frame * target.length + i * 7, true);
    idx = Math.floor(random(0, chars.length));
    result += chars[idx];
  }
}
result;
```

### Source Text — число с дрожащей последней цифрой

```javascript
baseVal = 9834;
fps     = thisComp.frameRate;
frame   = Math.floor(time * fps);
seedRandom(frame * 17, true);
lastDigit = Math.floor(random(0, 10));
// Меняем только последнюю цифру:
s = "" + baseVal;
s.slice(0, -1) + lastDigit;
```

### Per-character: случайная задержка появления каждой буквы

```javascript
// Text Layer -> Animation -> Add Animator -> Opacity
// Text Layer -> Animation -> Add -> Property -> Opacity
// Animator -> Range Selector -> Advanced -> Based On: Characters
// На Opacity Animator -> Opacity:
// (это через Text Animators, не expression напрямую на opacity)

// Альтернатива через Expression Selector:
// Animator -> Add -> Selector -> Expression
// В Expression Selector на Amount:
seedRandom(textIndex, true);
delay = random(0, 1.5);  // рандомная задержка для каждой буквы
t = clamp((time - delay) / 0.3, 0, 1);  // 0.3 сек на появление
t * 100;  // 0..100 -> Amount
```

### Source Text — форматирование числа с нулями (07 вместо 7)

```javascript
n = Math.floor(time * 10) % 100;  // пример: 0..99
n < 10 ? "0" + n : "" + n;
```

---

## 🖼️ SHAPE LAYERS — ШЕЙП-СЛОИ

> Shape layers — это мощь. Trim Paths, Path Points, Dash Pattern — всё под expression.

### Trim Paths End — "рисование" линии под бит

```javascript
// Shape -> Add -> Trim Paths -> End
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
// Линия "рисуется" под удар
```

### Trim Paths — бегущий огонёк (Start и End вместе)

```javascript
// На Trim Paths -> Start:
progress = (time * 0.3) % 1;   // скорость бега
segLen   = 0.15;                // длина огонька (15% от пути)
Math.max(0, progress - segLen) * 100;

// На Trim Paths -> End:
progress = (time * 0.3) % 1;
segLen   = 0.15;
Math.min(1, progress) * 100;
```

### Trim Paths End — с ускорением под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed  = 20;   // базовая скорость в % в секунду
beatBoost  = ease(amp, 0, 20, 0, 40);
speed      = baseSpeed + beatBoost;
// Накопительное заполнение:
clamp(value + speed * thisComp.frameDuration, 0, 100);
// ⚠️ value в Trim Paths — предыдущий кадр. Работает только с кейфреймом на 0 в начале.
```

### Rectangle Path Size — реактивный прямоугольник

```javascript
// Contents -> Rectangle -> Rectangle Path -> Size
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
w = ease(amp, 0, 20, 50, 400);
h = ease(amp, 0, 20, 50, 200);
[w, h];
```

### Rectangle Path — squash-stretch под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Чем громче — тем шире и ниже (сквош):
w = ease(amp, 0, 20, 100, 300);
h = ease(amp, 0, 20, 100, 40);
[w, h];
```

### Ellipse Path — пульсирующий круг → эллипс

```javascript
// Contents -> Ellipse -> Ellipse Path -> Size
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
// Левый канал -> X, правый -> Y: стерео-эллипс
rx = ease(L, 0, 20, 100, 250);
ry = ease(R, 0, 20, 100, 250);
[rx * 2, ry * 2];  // Size = диаметр, не радиус!
```

### Dash Pattern — мигающие пунктир

```javascript
// Contents -> Shape -> Stroke -> Dashes -> Dash
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 5, 50);
// Пунктир растёт на ударе
```

### Dash Offset — бегущий пунктир под бит

```javascript
// Contents -> Shape -> Stroke -> Dashes -> Offset
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed = 100;  // базовая скорость движения пунктира
beatSpeed = ease(amp, 0, 20, 0, 300);
(baseSpeed + beatSpeed) * time;
```

### Polystar — количество лучей под бит (Points)

```javascript
// Contents -> Polystar -> Polystar Path -> Points
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
Math.round(ease(amp, 0, 20, 3, 12));
// От 3 до 12 лучей! Math.round обязателен — Points должно быть целым
```

### Polystar Inner/Outer Radius под бит

```javascript
// Outer Radius:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 50, 200);

// Inner Radius (если Star, не Polygon):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 150, 20);
// При ударе — звезда схлопывается в иголки (inner < outer)
```

### Repeater Copies — количество повторений под бит

```javascript
// Contents -> Add -> Repeater -> Copies
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
Math.round(ease(amp, 0, 20, 1, 12));
// От 1 до 12 копий на ударе
```

### Repeater Transform -> Rotation — спиннер из копий

```javascript
// Contents -> Repeater -> Transform -> Rotation
360 / thisLayer.content("Repeater 1").copies;
// Каждая копия повёрнута равномерно по кругу — автоматически!
```

### Repeater Transform -> Position — радиус расширения

```javascript
// Contents -> Repeater -> Transform -> Position
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
r = ease(amp, 0, 20, 50, 200);
[r, 0];  // по X = радиус, при вращении копий -> круг
```

### Stroke -> Taper -> Start Width / End Width

```javascript
// Shape -> Stroke -> Taper -> Start Width (0..100%):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
// Обводка заостряется от начала на ударе
```

### Path — анимация вершин через expression (Bezier Points)

```javascript
// Contents -> Shape -> Path -> Path
// Нельзя напрямую менять точки через простой expression.
// Но можно: создай два кейфрейма Path (форма A и форма B)
// Потом на Path -> expression:
t = clamp(audioLayer.effect("Both Channels")("Slider") / 20, 0, 1);
// Это не работает напрямую — Path морфинг через expressions нативно не поддерживается.
// WORKAROUND: используй два Shape Layer с разными формами + Opacity на обоих:
// Layer A: opacity = ease(amp, 0,20, 100, 0)
// Layer B: opacity = ease(amp, 0,20, 0, 100)
// Визуально = морфинг формы под бит
```

---

## 🎬 TIME — РАБОТА СО ВРЕМЕНЕМ

> Время — это просто число. Его можно гнуть как угодно.

### Time Remap — стоп-кадр на ударе

```javascript
// Enable Time Remapping на footage layer
// Layer -> Time -> Enable Time Remapping
// На Time Remap expression:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// При ударе — замораживаем кадр:
freezeAmp = 15;  // порог заморозки
if (amp > freezeAmp) {
  // Возвращаем время последнего кадра до удара:
  value;  // value = предыдущий кейфреймовый time remap
} else {
  time;  // иначе идём нормально
}
```

### Time Remap — замедление на ударе (slowmo beat)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Чем громче — тем медленнее воспроизведение:
speedMult = ease(amp, 0, 20, 1.0, 0.1);  // от 100% до 10% скорости
// Интегрируем скорость: time remap = integral of speed
// Приближение через накопление:
value + speedMult * thisComp.frameDuration;
// ⚠️ Нужен кейфрейм в начале на 0!
```

### Time Remap — реверс видео на ударе

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 15;
if (amp > threshold) {
  // Идём назад:
  value - thisComp.frameDuration * 2;
} else {
  // Идём вперёд нормально:
  value + thisComp.frameDuration;
}
```

### Time Remap — случайный прыжок по видео

```javascript
// Видео скачет в рандомные точки на каждый удар
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
fps = thisComp.frameRate;
frame = Math.floor(time * fps);
seedRandom(frame, true);
if (amp > 18) {
  // Прыгаем в случайный момент видео (0..3 секунды):
  random(0, 3);
} else {
  time;
}
```

### Time Remap — стробоскоп (choppy fps)

```javascript
// Видео воспроизводится как будто с низким fps
targetFPS = 6;   // 6 кадров/сек — грубо, "стробо"
Math.floor(time * targetFPS) / targetFPS;
```

### Time Remap — стробоскоп интенсивнее под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Чем громче — тем грубее fps
targetFPS = ease(amp, 0, 20, 24, 3);  // от 24fps до 3fps на ударе
Math.floor(time * targetFPS) / targetFPS;
```

### Layer time — offset старта слоя через expression

```javascript
// Делает слой видимым с задержкой пропорционально index
delay = (index - 1) * 0.1;  // каждый следующий слой на 0.1 сек позже
// Используй Sequence Layers или In Point offset в AE
// Через expression: условие на Opacity:
time > inPoint + delay ? 100 : 0;
```

### Синхронизация с BPM через математику времени

```javascript
bpm         = 128;              // удары в минуту
secPerBeat  = 60 / bpm;        // секунд на бит
beatsElapsed = time / secPerBeat;
// Текущая доля бита (0..1):
beatFrac    = beatsElapsed % 1;
// Пульс на каждый бит (1 в начале, 0 в конце):
pulse = 1 - beatFrac;
// Вешай на Scale:
s = 100 + pulse * 30;
[s, s];
// Идеально синхронно с BPM — без аудио-слоя!
// ⚠️ Требует точного BPM трека
```

### BPM sync — со смещением (offset в долях бита)

```javascript
bpm        = 128;
offset     = 0.5;   // сдвиг на полбита (на "и" в счёте)
secPerBeat = 60 / bpm;
beatFrac   = ((time / secPerBeat) + offset) % 1;
pulse      = 1 - beatFrac;
s = 100 + pulse * 25;
[s, s];
```

### BPM sync — разные элементы на разные доли

```javascript
bpm        = 128;
secPerBeat = 60 / bpm;

// На первую долю такта (4/4):
beatInBar  = Math.floor((time / secPerBeat) % 4);
beatFrac   = (time / secPerBeat) % 1;

// Пульс только на 1-ю долю (kick):
if (beatInBar === 0) {
  s = 100 + (1 - beatFrac) * 50;
} else {
  s = 100;
}
[s, s];

// На 3-ю долю (snare):
// beatInBar === 2 ? s = 100 + ... : 100
```

---

## 📷 CAMERA — КАМЕРА

> 3D comp. Camera expressions — кинематика без кейфреймов.

### Camera Position — медленный кен-бёрнс (дрейф)

```javascript
// На Camera -> Position:
driftX = Math.sin(time * 0.1 * Math.PI * 2) * 50;
driftY = Math.cos(time * 0.07 * Math.PI * 2) * 30;
[value[0] + driftX, value[1] + driftY, value[2]];
// Камера плавно плывёт, никогда точно не повторяясь
```

### Camera Position — shake только под удар (не постоянно)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 30);
freq     = 18;
sx = Math.sin(time * freq * 6.28 * 1.0) * shakeAmt;
sy = Math.sin(time * freq * 6.28 * 1.3) * shakeAmt;
sz = Math.sin(time * freq * 6.28 * 0.7) * shakeAmt * 0.3;
[value[0] + sx, value[1] + sy, value[2] + sz];
```

### Camera Zoom (Z position) — динамический зум под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Z = расстояние камеры. Меньше Z = ближе = зум in
zoomIn = ease(amp, 0, 20, 0, 200);
[value[0], value[1], value[2] - zoomIn];
```

### Camera Focus Distance — расфокус под бит

```javascript
// Camera -> Options -> Focus Distance:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, value, value * 1.5);
// Фокус уходит на ударе — blurry hit effect
```

### Camera Aperture — глубина резкости под бит

```javascript
// Camera -> Options -> Aperture:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 50, 300);
// Больше апертура = сильнее размытие фона
```

### Camera Roll — крен камеры под бит

```javascript
// Camera -> Transform -> Z Rotation:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
maxRoll = ease(amp, 0, 20, 0, 5);
Math.sin(time * 3 * Math.PI * 2) * maxRoll;
// Камера покачивается, на ударе сильнее
```

### Camera — автоматический orbit вокруг null

```javascript
// Camera -> Point of Interest: привяжи к центральному нуллу
// Camera -> Position:
orbitRadius = 800;
orbitSpeed  = 0.15;  // оборотов в секунду
orbitHeight = -100;  // высота камеры
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
angle = time * orbitSpeed * Math.PI * 2;
[cx + Math.cos(angle) * orbitRadius,
 cy + orbitHeight,
 Math.sin(angle) * orbitRadius];
```

---

## 💡 LIGHTS — СВЕТ

### Light Intensity — пульс под бит

```javascript
// Light -> Options -> Intensity:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 50, 300);
// Свет вспыхивает на удар
```

### Light Color — смена цвета под бит

```javascript
// Light -> Options -> Color:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
t   = ease(amp, 0, 20, 0, 1);
// Интерполяция цвета от синего к красному:
r = t;
g = 0.2;
b = 1 - t;
[r, g, b, 1];
```

### Light Position — движение источника света

```javascript
// Point Light -> Position:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
orbitR = ease(amp, 0, 20, 100, 400);
speed  = 0.3;
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(time * speed * Math.PI * 2) * orbitR,
 cy + Math.sin(time * speed * Math.PI * 2) * orbitR * 0.5,
 -300];  // Z выше слоёв
```

### Light Cone Angle — пульсирующий прожектор

```javascript
// Spot Light -> Options -> Cone Angle:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 20, 90);
// На ударе прожектор раскрывается шире
```

---

## 🌀 3D — ТРЁХМЕРНОЕ ПРОСТРАНСТВО

### 3D Layer — вращение вокруг Y (поворот к камере)

```javascript
// 3D Layer -> Y Rotation:
freq = 0.2;
amp_ = 30;
Math.sin(time * freq * Math.PI * 2) * amp_;
// Слой качается вперёд-назад относительно камеры
```

### 3D Layer — параллакс-эффект (разная глубина под бит)

```javascript
// 3D Layer -> Z Position:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Разные слои летят с разной скоростью к камере:
seedRandom(index, true);
myDepth   = random(-500, 500);  // базовая глубина слоя
beatPush  = ease(amp, 0, 20, 0, 200);
myDepth - beatPush;
```

### 3D — orienting к камере (billboard)

```javascript
// 3D Layer -> Orientation или Auto-Orient:
// Через Auto-Orient -> Orient Towards Camera — включается в Layer menu
// Через expression на X/Y/Z Rotation:
cam = thisComp.activeCamera;
camPos  = cam.transform.position;
layPos  = transform.position;
// Вектор от слоя к камере:
diff = sub(camPos, layPos);
// Угол по Y:
Math.atan2(diff[0], diff[2]) * 180 / Math.PI;
```

### 3D Grid — позиция в сетке по index

```javascript
// Расставляет слои в 3D сетку автоматически
cols    = 5;       // столбцов
rows    = 4;       // строк
spacingX = 120;
spacingY = 120;
spacingZ = 80;

col = (index - 1) % cols;
row = Math.floor((index - 1) / cols) % rows;
dep = Math.floor((index - 1) / (cols * rows));

cx = thisComp.width  / 2;
cy = thisComp.height / 2;

[cx + (col - (cols-1)/2) * spacingX,
 cy + (row - (rows-1)/2) * spacingY,
 dep * spacingZ];
```

### 3D — расстояние от камеры -> scale (перспектива вручную)

```javascript
cam    = thisComp.activeCamera;
camPos = cam.transform.position;
layPos = transform.position;
dist   = length(camPos, layPos);
// Чем дальше — тем меньше:
s = ease(dist, 200, 1000, 150, 50);
[s, s];
```

---

## 🔢 COUNTERS & TIMERS — СЧЁТЧИКИ

### Простой счётчик (целые числа)

```javascript
// Считает от startVal до endVal за duration секунд
startVal = 0;
endVal   = 100;
duration = 2.0;
t  = clamp(time / duration, 0, 1);
Math.round(startVal + (endVal - startVal) * t);
```

### Счётчик с ease (разгон и торможение)

```javascript
startVal = 0;
endVal   = 9999;
duration = 3.0;
t   = clamp(time / duration, 0, 1);
st  = t * t * (3 - 2 * t);  // smoothstep
Math.round(startVal + (endVal - startVal) * st);
```

### Счётчик от аудио-удара (считает биты)

```javascript
// Нужен Slider Control "Beat Count" который ты вручную кейфреймируешь
// (или считай математически через BPM):
bpm      = 120;
beatNum  = Math.floor(time / (60 / bpm)) + 1;
"BEAT " + beatNum;
```

### Таймер — секундомер (MM:SS:FF)

```javascript
fps    = thisComp.frameRate;
totalFrames = Math.floor(time * fps);
ff = totalFrames % Math.round(fps);
ss = Math.floor(time) % 60;
mm = Math.floor(time / 60);
function pad(n) { return n < 10 ? "0" + n : "" + n; }
pad(mm) + ":" + pad(ss) + ":" + pad(ff);
```

### Прогресс-бар через Trim Paths + счётчик

```javascript
// На Trim Paths -> End (прогресс-бар форма):
duration = 10.0;
clamp(time / duration * 100, 0, 100);

// На Text Layer рядом (процент):
duration = 10.0;
Math.round(clamp(time / duration * 100, 0, 100)) + "%";
```

### Countdown с миганием последних секунд

```javascript
totalSec  = 10;
remaining = Math.max(0, totalSec - time);
secs      = Math.ceil(remaining);

// Мигание когда < 3 секунд:
if (remaining < 3) {
  fps   = thisComp.frameRate;
  blink = Math.floor(time * fps * 2) % 2;  // мигает 2 раза в секунду
  opacity = blink ? 100 : 20;
} else {
  opacity = 100;
}
// Вешай на Opacity: opacity
// На Source Text: "" + secs
```

### Числовой одометр (ролики цифр)

```javascript
// Для каждого "ролика" (отдельный текстовый слой):
// Слой "Digit_1" — единицы, "Digit_10" — десятки, etc.

totalVal = 1234;   // итоговое значение
duration = 2.0;
t  = clamp(time / duration, 0, 1);
st = t * t * (3 - 2 * t);
curVal = Math.round(st * totalVal);

// Для слоя единиц: curVal % 10
// Для слоя десятков: Math.floor(curVal / 10) % 10
// Для слоя сотен: Math.floor(curVal / 100) % 10
// Для слоя тысяч: Math.floor(curVal / 1000) % 10
"" + (curVal % 10);  // на слой единиц
```

---

## 🎨 EFFECTS — КОНКРЕТНЫЕ ЭФФЕКТЫ

> Конкретные экспрешены под конкретные эффекты. Никакой воды.

### Gaussian Blur — размытие под бит

```javascript
// Effect -> Gaussian Blur -> Blurriness:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 40);
```

### Gaussian Blur — расфокус в тишине, чёткость на ударе

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 30, 0);  // инвертировано!
```

### Directional Blur — направленное размытие под движение

```javascript
// Effect -> Directional Blur -> Blur Length:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 60);

// Directional Blur -> Direction (угол размытия):
// Если объект движется по X — ставь 90°
// Если по Y — 0°
// Динамически под движение:
posNow  = transform.position;
posPrev = transform.position.valueAtTime(time - thisComp.frameDuration);
diff    = sub(posNow, posPrev);
Math.atan2(diff[1], diff[0]) * 180 / Math.PI + 90;
```

### Chromatic Aberration (через Shift Channels / CC) — глитч

```javascript
// Нет нативного CA в AE, симулируем через:
// Дублируй слой 3 раза (R, G, B)
// На каждый — Set Channels effect, оставь только свой канал
// На Position каждого:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
caAmt = ease(amp, 0, 20, 0, 8);

// R-слой:
[value[0] - caAmt, value[1]];
// G-слой:
[value[0], value[1]];
// B-слой:
[value[0] + caAmt, value[1]];
```

### Glow Intensity под бит (Effect -> Glow -> Glow Intensity)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0.5, 3.0);
```

### Glow Radius под бит

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 5, 80);
```

### Turbulent Displace — искажение под бит

```javascript
// Effect -> Turbulent Displace -> Amount:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 60);

// Evolution (непрерывное движение шума):
// Effect -> Turbulent Displace -> Evolution:
time * 200;  // градусов в секунду

// Evolution быстрее под бит:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseEvo  = time * 100;
beatEvo  = ease(amp, 0, 20, 0, 500);
baseEvo + beatEvo;
```

### CC Pixel Polly (рассыпание) — сила под бит

```javascript
// Effect -> CC Pixel Polly -> Force:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 5);
```

### Wave Warp — амплитуда волны под бит

```javascript
// Effect -> Wave Warp -> Wave Height:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 50);

// Wave Speed:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0.5, 5.0);
```

### Hue/Saturation — насыщенность под бит

```javascript
// Effect -> Hue/Saturation -> Master Saturation:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, -50, 100);
// В тишине — обесцвеченный, на ударе — яркий
```

### Hue/Saturation — оттенок крутится по кругу

```javascript
// Master Hue:
time * 60;  // 60 градусов в секунду = полный оборот за 6 сек

// Быстрее под бит:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed = 30;
beatBoost = ease(amp, 0, 20, 0, 200);
(baseSpeed + beatBoost) * time;
```

### Brightness & Contrast — вспышка на удар

```javascript
// Effect -> Brightness & Contrast -> Brightness:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 80);
```

### Posterize Time — choppy под бит (Effect -> Time -> Posterize Time)

```javascript
// Posterize Time -> Frame Rate:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 24, 4);
// В тишине — плавно, на ударе — рывками как 4fps
```

### Echo — количество отражений под бит

```javascript
// Effect -> Time -> Echo -> Number Of Echoes:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
Math.round(ease(amp, 0, 20, 0, 8));
```

### CC Radial Fast Blur — вспышка zoom blur

```javascript
// Effect -> CC Radial Fast Blur -> Amount:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 80);
```

### Fractal Noise — эволюция под бит

```javascript
// Effect -> Noise & Grain -> Fractal Noise -> Evolution:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed = time * 90;
beatSpeed = ease(amp, 0, 20, 0, 400);
baseSpeed + beatSpeed;
```

### Fractal Noise — масштаб под бит

```javascript
// Fractal Noise -> Transform -> Scale:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 400);
```

### Displacement Map (внешний слой) — сила смещения

```javascript
// Effect -> Distort -> Displacement Map -> Max Horizontal Displacement:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 40);
```

---

## 📐 MASKS & TRIM PATHS — МАСКИ И ОБРЕЗКА

### Mask Expansion — маска расширяется под бит

```javascript
// Layer -> Mask -> Mask Expansion:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 80);
// Маска раздувается на удар, открывая больше слоя
```

### Mask Feather — мягкость края под бит

```javascript
// Layer -> Mask -> Mask Feather:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
f = ease(amp, 0, 20, 0, 60);
[f, f];  // Feather — это массив [horizontal, vertical]
```

### Mask Opacity — появление через маску

```javascript
// Layer -> Mask -> Mask Opacity:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```

### Mask Path — маска дышит (через Mask Expansion + sin)

```javascript
// Mask Expansion:
freq = 1.2;
range = 20;
Math.sin(time * freq * Math.PI * 2) * range;
// Маска органично дышит туда-сюда
```

### Trim Paths — телеграф (morse code через expression)

```javascript
// Shape -> Add -> Trim Paths -> End
// Можно кодировать паттерн через массив:
pattern = [1, 0, 1, 1, 0, 1, 0, 0];  // 1=линия, 0=пауза
dotDur  = 0.1;  // длительность одного элемента
totalDur = pattern.length * dotDur;
t = time % totalDur;  // зацикливаем
idx = Math.floor(t / dotDur);
pattern[idx] * 100;  // 100 или 0
```

### Trim Paths — нарисовать-стереть-нарисовать (loop)

```javascript
// End:
cycleDur = 2.0;  // полный цикл
halfDur  = cycleDur / 2;
t        = time % cycleDur;
if (t < halfDur) {
  // Рисуем (0 -> 100):
  (t / halfDur) * 100;
} else {
  // Стираем (100 -> 0):
  (1 - (t - halfDur) / halfDur) * 100;
}

// Start (всегда 0 при рисовании, нагоняет при стирании):
cycleDur = 2.0;
halfDur  = cycleDur / 2;
t        = time % cycleDur;
if (t < halfDur) {
  0;
} else {
  ((t - halfDur) / halfDur) * 100;
}
```

### Trim Paths — разные фазы на разных слоях (stagger)

```javascript
// На каждом слое-линии -> Trim Paths -> End:
// Каждый начинает рисоваться чуть позже
staggerDelay = (index - 1) * 0.15;
drawDur      = 0.8;
t = clamp((time - staggerDelay) / drawDur, 0, 1);
st = t * t * (3 - 2 * t);
st * 100;
```

### Mask + Beat — открываемся на бит (радиальная маска)

```javascript
// Elliptical Mask -> Mask Expansion:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Маска мала в тишине, открывается на удар:
ease(amp, 0, 20, -200, 100);
// -200 = полностью закрыта (Inverted mask), 100 = расширена
```

---

## 🧮 MATH PATTERNS — МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ

> Специфические математические трюки которые дают уникальные эффекты.

### Golden Ratio spiral (расстановка по золотой спирали)

```javascript
// Расставляет N объектов по спирали Фибоначчи
phi     = (1 + Math.sqrt(5)) / 2;           // золотое сечение
goldenAngle = Math.PI * 2 * (2 - phi);       // ~137.5 градусов
n       = index - 1;
radius  = Math.sqrt(n) * 30;                 // радиус нарастает
angle   = n * goldenAngle;
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
// Классическое расположение семян подсолнуха
```

### Fibonacci sequence — размеры по Фибоначчи

```javascript
// index 1..10 -> числа Фибоначчи как scale
function fib(n) {
  a = 1; b = 1;
  for (i = 2; i < n; i++) {
    c = a + b; a = b; b = c;
  }
  return b;
}
fibVal = fib(index);
s = Math.min(fibVal * 5, 200);  // ограничиваем максимум
[s, s];
```

### Noise field — разные направления движения у толпы

```javascript
// У каждого объекта направление определяется его позицией в "поле шума"
// Имитация через два вигла с разными seed:
seedRandom(index * 100, false);  // false = меняется со временем
noiseX = wiggle(0.3, 100)[0];
noiseY = wiggle(0.3, 100)[1];
[value[0] + noiseX, value[1] + noiseY];
// Объекты текут как в поле ветра
```

### Sine table — дискретный шаговый синус

```javascript
// 8 шагов синуса — ступенчатая волна
steps  = 8;
period = 2.0;  // секунд на цикл
t      = (time / period) % 1;
step   = Math.floor(t * steps) / steps;  // дискретизируем
Math.sin(step * Math.PI * 2) * 100;
```

### Chladni-паттерн (стоячие волны) — для текстур

```javascript
// Имитация паттернов Хладни через синусы
// Вешай на Position или через Displacement Map с этим значением
m = 3;  n = 4;  // параметры формы (менять = разные паттерны)
// Это для условия: Math.abs(sin(m*PI*x)*sin(n*PI*y)) < threshold
// Как маска — нужна Custom Effect или через Expression на Mask:
// Проще: используй как Evolution в Fractal Noise:
time * m * 37 + Math.sin(time * n * 29) * 180;
```

### Perlin-like через сложение синусов (без wiggle)

```javascript
// Детерминированный "шум" через сумму синусов с разными частотами
// Преимущество: воспроизводимо, управляемо, без seed
t     = time;
noise = Math.sin(t * 1.00 * Math.PI * 2) * 0.500
      + Math.sin(t * 2.13 * Math.PI * 2) * 0.250
      + Math.sin(t * 4.23 * Math.PI * 2) * 0.125
      + Math.sin(t * 8.37 * Math.PI * 2) * 0.0625
      + Math.sin(t * 16.7 * Math.PI * 2) * 0.03125;
// noise в диапазоне ~-1..1
noise * 80;  // масштабируй под нужный диапазон
```

### Beat quantization — привязка движения к сетке бита

```javascript
// Движение происходит только в моменты бита, иначе стоит
bpm       = 120;
secPerBeat = 60 / bpm;
// Квантизованное время — прыгает на каждом бите:
quantTime  = Math.floor(time / secPerBeat) * secPerBeat;
// Синус, но только обновляющийся раз в бит:
seedRandom(Math.floor(time / secPerBeat), true);
targetX = random(-200, 200);
targetY = random(-100, 100);
// Плавно едем к рандомной точке за один бит:
t = (time % secPerBeat) / secPerBeat;
st = t * t * (3 - 2 * t);
// Для X (нужно знать прошлую позицию — сложно без кейфреймов)
// Упрощённо: прыжок в рандомную точку:
seedRandom(Math.floor(time / secPerBeat) * 100 + index, true);
value[0] + random(-100, 100) * (1 / thisComp.frameRate / secPerBeat);
// ⚠️ Эта тема требует Slider Control для хранения предыдущего состояния
```

### Harmonics — несколько объектов на гармониках частоты

```javascript
// Каждый слой — следующая гармоника основной частоты
fundamental = 0.5;  // базовая частота в Гц
harmonic    = index;  // 1, 2, 3, 4... — для каждого слоя
freq_       = fundamental * harmonic;
amp_        = 50 / harmonic;  // амплитуда убывает
Math.sin(time * freq_ * Math.PI * 2) * amp_;
// Слои образуют гармонический ряд — как обертоны звука
```

### Модуляция частоты (FM синтез визуально)

```javascript
// Несущая частота модулируется другой частотой
carrierFreq = 2.0;   // несущая
modFreq     = 0.3;   // модулятор
modDepth    = 50;    // глубина модуляции (диапазон)
amp_        = 80;

// Мгновенная частота = carrier + modulator * depth:
modulator  = Math.sin(time * modFreq * Math.PI * 2) * modDepth;
// Интеграл несущей с переменной частотой:
phase      = carrierFreq * time + modulator * time * 0.5;
Math.sin(phase * Math.PI * 2) * amp_;
// Звучит и выглядит как FM — сложные, живые паттерны
```

### Chord — несколько слоёв на музыкальных интервалах

```javascript
// Если fundamental = visual tempo, то интервалы задают "аккорд" движения
fundamental = 0.5;
// Мажорный аккорд: 1, 5/4, 3/2 (унисон, терция, квинта)
intervals   = [1, 1.25, 1.5, 2.0];
myInterval  = intervals[(index - 1) % intervals.length];
freq_       = fundamental * myInterval;
Math.sin(time * freq_ * Math.PI * 2) * 60;
// Каждый слой на своём интервале — визуальная гармония
```

---

## 🏗️ MASTER RIG v2 — PRODUCTION FULL RIG

> Полный боевой риг. Ставишь один раз — управляешь всем.

### Структура MASTER RIG v2

```
[NULL "BEAT_MASTER"]
  ├── Slider "Beat Raw"        <- сырая амплитуда
  ├── Slider "Beat Smooth"     <- сглаженная (0..100)
  ├── Slider "Beat Sharp"      <- резкая (easeOut)
  ├── Slider "Energy"          <- глобальная интенсивность (0..100)
  ├── Slider "BPM"             <- ручной BPM для синхронизации
  ├── Slider "Freq Base"       <- базовая частота синусов
  ├── Checkbox "Enable Beat"   <- вкл/выкл реакцию на аудио
  ├── Checkbox "Enable Proc"   <- вкл/выкл процедурное движение
  └── Checkbox "Enable Wiggle" <- вкл/выкл wiggle

[NULL "PROC_MASTER"]  <- отдельно для процедурного движения
  ├── Slider "Drift Speed"     <- скорость органичного дрейфа
  ├── Slider "Drift Amp"       <- амплитуда дрейфа
  ├── Slider "Pulse Freq"      <- частота пульсации
  ├── Slider "Pulse Amp"       <- амплитуда пульсации
  └── Point  "Target"          <- глобальная точка притяжения
```

### BEAT_MASTER -> Beat Raw

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
audioLayer.effect("Both Channels")("Slider");
```

### BEAT_MASTER -> Beat Smooth

```javascript
raw = thisLayer.effect("Beat Raw")("Slider");
ease(raw, 0, 20, 0, 100);
```

### BEAT_MASTER -> Beat Sharp

```javascript
raw = thisLayer.effect("Beat Raw")("Slider");
easeOut(raw, 0, 20, 0, 100);
// Быстрая атака, плавное затухание — для ударных акцентов
```

### Использование на слоях — Scale через Beat Smooth

```javascript
M = thisComp.layer("BEAT_MASTER");
energy  = M.effect("Energy")("Slider") / 100;
enabled = M.effect("Enable Beat")("Checkbox");
beat    = M.effect("Beat Smooth")("Slider");

if (enabled) {
  s = ease(beat, 0, 100, 100, 100 + 60 * energy);
} else {
  s = 100;
}
[s, s];
```

### Использование — Position с процедурным дрейфом

```javascript
M = thisComp.layer("BEAT_MASTER");
P = thisComp.layer("PROC_MASTER");

// Бит-компонент:
beatEnabled = M.effect("Enable Beat")("Checkbox");
beat        = M.effect("Beat Sharp")("Slider");
energy      = M.effect("Energy")("Slider") / 100;
beatOffsetY = beatEnabled ? ease(beat, 0, 100, 0, -50 * energy) : 0;

// Процедурный компонент:
procEnabled = P.effect("Enable Proc")("Checkbox");
driftSpeed  = P.effect("Drift Speed")("Slider");
driftAmp    = P.effect("Drift Amp")("Slider");

// Случайная фаза для этого слоя:
seedRandom(index * 31, true);
phaseX = random(0, Math.PI * 2);
phaseY = random(0, Math.PI * 2);

procOffsetX = procEnabled ? Math.sin(time * driftSpeed * Math.PI * 2 + phaseX) * driftAmp : 0;
procOffsetY = procEnabled ? Math.sin(time * driftSpeed * Math.PI * 2 * 0.7 + phaseY) * driftAmp * 0.6 : 0;

// Итог:
[value[0] + procOffsetX, value[1] + procOffsetY + beatOffsetY];
```

### Использование — Rotation комбо

```javascript
M = thisComp.layer("BEAT_MASTER");
P = thisComp.layer("PROC_MASTER");

beat       = M.effect("Beat Smooth")("Slider");
energy     = M.effect("Energy")("Slider") / 100;
pulseFreq  = P.effect("Pulse Freq")("Slider");
pulseAmp   = P.effect("Pulse Amp")("Slider");

seedRandom(index * 17, true);
phase = random(0, Math.PI * 2);

// Процедурное качание:
procRot = Math.sin(time * pulseFreq * Math.PI * 2 + phase) * pulseAmp;
// Бит-поворот:
beatRot = ease(beat, 0, 100, 0, 15 * energy);

procRot + beatRot;
```

### Использование — Opacity с порогом и энергией

```javascript
M = thisComp.layer("BEAT_MASTER");
beat   = M.effect("Beat Smooth")("Slider");
energy = M.effect("Energy")("Slider") / 100;

// Базовая прозрачность + вспышка под бит:
baseOpacity = 60;
beatFlash   = ease(beat, 0, 100, 0, 40 * energy);
clamp(baseOpacity + beatFlash, 0, 100);
```

### BPM sync через BEAT_MASTER

```javascript
M       = thisComp.layer("BEAT_MASTER");
bpm_    = M.effect("BPM")("Slider");     // значение BPM установлено вручную
energy  = M.effect("Energy")("Slider") / 100;

secPerBeat = 60 / bpm_;
beatFrac   = (time / secPerBeat) % 1;
// Пульс: 1 в начале бита, 0 к концу:
pulse = Math.pow(1 - beatFrac, 2);  // квадратичное затухание
s = 100 + pulse * 40 * energy;
[s, s];
```

### Итоговый чеклист при работе с MASTER RIG v2

```
□ Создан NULL "BEAT_MASTER" со всеми Slider/Checkbox controls
□ Создан NULL "PROC_MASTER" со своими controls  
□ На BEAT_MASTER -> Beat Raw -> аудио expression
□ На BEAT_MASTER -> Beat Smooth -> ease от Raw
□ На BEAT_MASTER -> Beat Sharp -> easeOut от Raw
□ Energy Slider = 50 (можно кейфреймировать для sections)
□ BPM Slider = реальный BPM трека
□ Все рабочие слои ссылаются ТОЛЬКО на BEAT_MASTER и PROC_MASTER
□ НЕ одна прямая ссылка на Audio Amplitude из рабочих слоёв
□ Enable Beat / Enable Proc / Enable Wiggle — тестируй по очереди
```

---

## 🎵 FREQUENCY BANDS — ЧАСТОТНЫЕ ДИАПАЗОНЫ

> Convert Audio to Keyframes даёт тебе ALL, LEFT, RIGHT — но не разбивку по частотам. Вот как это обойти.

### Проблема: один канал = всё вместе (kick + hihat + bass)

```javascript
// Both Channels — сумма ВСЕГО спектра.
// Чтобы реагировать на бас отдельно от хетов — нужен EQ трюк.
// Воркфлоу:
// 1. Дублируй аудио-слой N раз (по числу диапазонов)
// 2. На каждый дубль — Effect -> Audio -> Parametric EQ
// 3. Вырежи нужный диапазон (только бас, только мид, только хай)
// 4. Запусти Convert Audio to Keyframes для каждого дубля
// 5. Получишь отдельные слои [Audio Amplitude] для каждого диапазона
```

### Типовые диапазоны для EQ

```javascript
// Sub Bass:    20  – 80  Hz   (kick body, бочка)
// Bass:        80  – 250 Hz   (бас-гитара, нижний мид)
// Low Mid:     250 – 800 Hz   (тело голоса, гитары)
// High Mid:    800 – 4000 Hz  (атака, presence)
// High:        4000 – 20000 Hz (хеты, тарелки, воздух)
```

### Риг с тремя частотными слоями

```javascript
// Допустим у тебя три слоя с амплитудами:
// "Amp_Bass"  — только низкие (бочка, бас)
// "Amp_Mid"   — средние
// "Amp_High"  — высокие (хеты)

bassAmp = thisComp.layer("Amp_Bass").effect("Both Channels")("Slider");
midAmp  = thisComp.layer("Amp_Mid").effect("Both Channels")("Slider");
highAmp = thisComp.layer("Amp_High").effect("Both Channels")("Slider");

// Scale реагирует только на бас:
s = ease(bassAmp, 0, 20, 100, 160);
[s, s];
```

### Position X — хеты двигают по горизонтали

```javascript
highAmp = thisComp.layer("Amp_High").effect("Both Channels")("Slider");
ox = ease(highAmp, 0, 15, 0, 40);
[value[0] + ox, value[1]];
```

### Rotation — мид-частоты крутят

```javascript
midAmp = thisComp.layer("Amp_Mid").effect("Both Channels")("Slider");
ease(midAmp, 0, 18, 0, 25);
```

### Три объекта на три частоты (независимые)

```javascript
// Объект 1 (Scale) — только бас:
bassAmp = thisComp.layer("Amp_Bass").effect("Both Channels")("Slider");
s = ease(bassAmp, 0, 20, 100, 180);
[s, s];

// Объект 2 (Opacity) — только хеты:
highAmp = thisComp.layer("Amp_High").effect("Both Channels")("Slider");
ease(highAmp, 0, 15, 40, 100);

// Объект 3 (Position Y) — мидранж:
midAmp = thisComp.layer("Amp_Mid").effect("Both Channels")("Slider");
oy = ease(midAmp, 0, 18, 0, -60);
[value[0], value[1] + oy];
```

### Имитация частотного разделения без дубликатов (грязный хак)

```javascript
// Both Channels хорошо ловит удар бочки (доминирует в низах).
// Left Channel иногда отличается от Right на стерео-записях.
// Трюк: Left-Right разность = что уходит в стороны (обычно хеты/пэды)
audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
B = audioLayer.effect("Both Channels")("Slider");

lowProxy  = B;               // Both ≈ доминирует бас
highProxy = Math.abs(L - R); // разность ≈ стерео-компонент (часто хеты)

// Используй highProxy для реакции на хеты:
s = ease(highProxy, 0, 5, 100, 140);
[s, s];
```

---

## 👥 CROWD RIG — ТОЛПЫ И МАССИВЫ

> 50 одинаковых объектов. Каждый ведёт себя по-своему. Без единого кейфрейма.

### Базовый принцип: index + seedRandom = уникальность

```javascript
// index — номер слоя в comp (1, 2, 3...)
// seedRandom(seed, timeless) — инициализирует генератор
// После seedRandom -> random() даст одно и то же число для этого слоя
seedRandom(index * 137, true);  // 137 — простое число, хорошо распределяет
myRandom = random(0, 1);        // у каждого слоя своё, от 0 до 1
```

### Расстановка в ряд (горизонталь)

```javascript
// N слоёв равномерно по горизонтали:
totalLayers = 10;
spacing     = 100;
startX      = thisComp.width / 2 - (totalLayers - 1) * spacing / 2;
x = startX + (index - 1) * spacing;
[x, thisComp.height / 2];
```

### Расстановка в сетку (grid) по index

```javascript
cols     = 8;
spacing  = 90;
startX   = thisComp.width  / 2 - ((cols - 1) * spacing) / 2;
startY   = thisComp.height / 2 - (Math.floor(thisComp.numLayers / cols) * spacing) / 2;

col = (index - 1) % cols;
row = Math.floor((index - 1) / cols);

[startX + col * spacing, startY + row * spacing];
```

### Расстановка по кругу

```javascript
n       = thisComp.numLayers;  // общее кол-во слоёв
radius  = 300;
angle   = ((index - 1) / n) * Math.PI * 2;
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
```

### Расстановка по кругу + вращение всей группы

```javascript
n       = thisComp.numLayers;
radius  = 280;
rotSpeed = 0.1;  // оборотов в секунду всей группы
baseAngle = ((index - 1) / n) * Math.PI * 2;
groupAngle = time * rotSpeed * Math.PI * 2;
cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(baseAngle + groupAngle) * radius,
 cy + Math.sin(baseAngle + groupAngle) * radius];
```

### Stagger появления — каждый возникает с задержкой

```javascript
// На Opacity каждого слоя:
staggerDelay = (index - 1) * 0.08;  // 80ms между слоями
fadeDur      = 0.4;
t = clamp((time - staggerDelay) / fadeDur, 0, 1);
st = t * t * (3 - 2 * t);
st * 100;
```

### Stagger с рандомной задержкой (не равномерно)

```javascript
seedRandom(index * 53, true);
delay  = random(0, 1.5);
fadeDur = 0.3;
t = clamp((time - delay) / fadeDur, 0, 1);
st = t * t * (3 - 2 * t);
st * 100;
```

### Волна по рядам (wave через index)

```javascript
// Scale волной проходит по всем слоям:
freq      = 1.2;   // скорость волны
waveAmp   = 40;    // амплитуда волны
phaseStep = 0.3;   // фаза сдвига между соседними слоями

phase = (index - 1) * phaseStep;
s = 100 + Math.sin(time * freq * Math.PI * 2 - phase) * waveAmp;
[s, s];
```

### Волна по кругу (radial wave)

```javascript
// Слои по кругу, волна идёт по окружности:
n         = thisComp.numLayers;
freq      = 0.8;
waveAmp   = 50;
baseAngle = ((index - 1) / n) * Math.PI * 2;

// Фаза = угол слоя:
s = 100 + Math.sin(time * freq * Math.PI * 2 - baseAngle * 2) * waveAmp;
[s, s];
```

### Beat + stagger: каждый реагирует на бит со своей задержкой

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
// Случайная задержка (lag) для каждого слоя:
seedRandom(index * 29, true);
lag = random(0, 0.25);
delayedAmp = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - lag);
s = ease(delayedAmp, 0, 20, 80, 160);
[s, s];
```

### Инверсия паттерна через чётность index

```javascript
// Чётные и нечётные слои реагируют в противофазе:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

if (index % 2 === 0) {
  // Чётные: вниз
  oy = ease(amp, 0, 20, 0, 60);
} else {
  // Нечётные: вверх
  oy = ease(amp, 0, 20, 0, -60);
}
[value[0], value[1] + oy];
```

### Каскадный scale от центра (ripple)

```javascript
// Слои расположены по кругу или в ряд
// "Волна" расходится от центрального слоя:
centerIndex = Math.ceil(thisComp.numLayers / 2);
distFromCenter = Math.abs(index - centerIndex);
travelSpeed = 5;  // слоёв в секунду
delay = distFromCenter / travelSpeed;

audioLayer = thisComp.layer("Audio Amplitude");
delayedAmp = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - delay);
s = ease(delayedAmp, 0, 20, 90, 160);
[s, s];
```

### Рандомный цвет из палитры для каждого слоя

```javascript
// Fill Color на Shape Layer:
palette = [
  [1.0, 0.2, 0.2, 1],  // красный
  [0.2, 0.8, 1.0, 1],  // голубой
  [1.0, 0.9, 0.1, 1],  // жёлтый
  [0.3, 1.0, 0.4, 1],  // зелёный
  [0.9, 0.3, 1.0, 1],  // фиолетовый
];
seedRandom(index * 71, true);
paletteIndex = Math.floor(random(0, palette.length));
palette[paletteIndex];
```

### Рандомный scale при старте (разные размеры у объектов)

```javascript
seedRandom(index * 43, true);
baseScale = random(60, 140);

// + бит сверху:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
beatBoost = ease(amp, 0, 20, 0, 30);

s = baseScale + beatBoost;
[s, s];
```

### Толпа: position drift с уникальным паттерном у каждого

```javascript
seedRandom(index * 97, true);
freqX  = random(0.2, 0.9);
freqY  = random(0.15, 0.7);
ampX   = random(20, 80);
ampY   = random(15, 60);
phaseX = random(0, Math.PI * 2);
phaseY = random(0, Math.PI * 2);

ox = Math.sin(time * freqX * Math.PI * 2 + phaseX) * ampX;
oy = Math.sin(time * freqY * Math.PI * 2 + phaseY) * ampY;
[value[0] + ox, value[1] + oy];
```

### Пульс с задержкой по спирали (spiral stagger)

```javascript
// Объекты расположены по спирали, пульс идёт от центра наружу:
n           = thisComp.numLayers;
spiralPhase = ((index - 1) / n) * Math.PI * 6;  // 3 оборота спирали
delay       = spiralPhase / (Math.PI * 2) * 0.5; // 0.5 сек на оборот

audioLayer  = thisComp.layer("Audio Amplitude");
delayedAmp  = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - delay);
s = ease(delayedAmp, 0, 20, 80, 160);
[s, s];
```

---

## ⚓ ANCHOR POINT — ТОЧКА ТРАНСФОРМАЦИИ

> Anchor Point определяет откуда Scale и Rotation. Меняешь его — полностью меняешь характер анимации.

### Anchor Point в угол (трансформация от угла)

```javascript
// Anchor Point -> [0, 0] = левый верхний угол слоя
// Anchor Point -> [w, h] = правый нижний угол
// Авто через size:
w = sourceRectAtTime(time).width;
h = sourceRectAtTime(time).height;

// Левый нижний угол (как текст растёт вверх):
[0, h];
// Правый верхний:
[w, 0];
// По центру (дефолт):
[w / 2, h / 2];
```

### Anchor Point по центру слоя (надёжный способ)

```javascript
// Иногда AE ставит AP не в центр. Фиксим:
r = sourceRectAtTime(time);
[r.left + r.width / 2, r.top + r.height / 2];
```

### Anchor Point динамически — вращение вокруг края

```javascript
// Rotation вокруг правого края:
w = sourceRectAtTime(time).width;
h = sourceRectAtTime(time).height;
[w, h / 2];
// Слой будет "распахиваться" как дверь
```

### Anchor Point под бит — смена точки трансформации

```javascript
// AP прыгает от центра к краю на ударе:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
r   = sourceRectAtTime(time);
w   = r.width;
h   = r.height;

cx = w / 2;
cy = h / 2;
ex = w;   // правый край
ey = h / 2;

t = ease(amp, 0, 20, 0, 1);
[cx + (ex - cx) * t, cy + (ey - cy) * t];
// AP плавно едет от центра к правому краю на ударе
```

### Position компенсация при смене Anchor Point

```javascript
// Когда меняешь AP — слой "прыгает" на экране.
// Чтобы слой остался на месте — компенсируй Position:
// Сначала фиксируй нужный AP, потом пересчитывай Position:
// Position += (new_AP - old_AP) rotated by layer rotation
// Это делается вручную или через Effect -> Transform
```

### Rotating array — каждый слой вращается вокруг своей точки по кругу

```javascript
// AP = конец "спицы", слой = точка на спице
// Scale слоя = длина спицы
n      = 12;
radius = 200;
speed  = 0.3;
myAngle = ((index - 1) / n) * Math.PI * 2 + time * speed * Math.PI * 2;

cx = thisComp.width  / 2;
cy = thisComp.height / 2;

// Position = центр + вектор вдоль спицы:
// AP ставим в конец слоя [width, height/2]
// Position:
[cx + Math.cos(myAngle) * radius,
 cy + Math.sin(myAngle) * radius];
// Rotation:
// myAngle * 180 / Math.PI;  — на Rotation property
```

---

## 🎞️ COMP MARKERS — МАРКЕРЫ КОМПА

> Маркеры — самый недооценённый инструмент. Можно делать event-driven анимацию.

### Базовый доступ к маркеру

```javascript
// thisComp.marker — объект с маркерами
// thisComp.marker.numKeys — количество маркеров
// thisComp.marker.key(index) — маркер по номеру
// thisComp.marker.key(index).time — время маркера
// thisComp.marker.key(index).comment — текстовая метка

// Ближайший маркер до текущего момента:
lastMarker = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  if (thisComp.marker.key(i).time <= time) {
    lastMarker = thisComp.marker.key(i).time;
  }
}
lastMarker;  // время последнего прошедшего маркера
```

### Пульс на каждом маркере (elapsed time from marker)

```javascript
// Сколько секунд прошло с последнего маркера:
lastMarkerTime = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  t = thisComp.marker.key(i).time;
  if (t <= time && t > lastMarkerTime) {
    lastMarkerTime = t;
  }
}
elapsed = time - lastMarkerTime;

// Затухающий пульс на каждом маркере:
decay   = 3.0;
initAmp = 50;
initAmp * Math.exp(-decay * elapsed);
```

### Scale bounce на каждом маркере

```javascript
lastMarkerTime = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  t = thisComp.marker.key(i).time;
  if (t <= time) lastMarkerTime = t;
}
elapsed  = time - lastMarkerTime;
decay    = 5.0;
freq     = 4.0;
bounce   = Math.exp(-decay * elapsed) * Math.cos(freq * Math.PI * 2 * elapsed);
s = 100 + bounce * 30;
[s, s];
// На каждый маркер — объект "пружинит"
```

### Transition по маркеру — смена состояния

```javascript
// Маркер 1: начало секции A
// Маркер 2: начало секции B
// На Opacity слоя:

sectionA_end = thisComp.marker.numKeys >= 2
               ? thisComp.marker.key(2).time
               : 9999;

transitionDur = 0.5;
if (time < sectionA_end - transitionDur) {
  100;  // секция A — видим
} else if (time < sectionA_end) {
  // плавный выход:
  ease(time, sectionA_end - transitionDur, sectionA_end, 100, 0);
} else {
  0;    // секция B — скрыт
}
```

### Счётчик прошедших маркеров

```javascript
count = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  if (thisComp.marker.key(i).time <= time) count++;
}
"Section " + count;
// Source Text показывает номер текущей секции
```

### Цвет меняется по маркеру (каждая секция — свой цвет)

```javascript
// Fill Color:
colors = [
  [1.0, 0.2, 0.2, 1],  // красный
  [0.2, 0.6, 1.0, 1],  // синий
  [0.2, 1.0, 0.4, 1],  // зелёный
  [1.0, 0.9, 0.1, 1],  // жёлтый
];

currentSection = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  if (thisComp.marker.key(i).time <= time) currentSection++;
}
idx = currentSection % colors.length;
colors[idx];
```

### Скорость wiggle меняется по маркеру

```javascript
// Каждая секция — другой темп wiggle
lastMarkerIdx = 0;
for (i = 1; i <= thisComp.marker.numKeys; i++) {
  if (thisComp.marker.key(i).time <= time) lastMarkerIdx = i;
}

// Разные частоты по секциям:
freqs = [0.5, 2.0, 8.0, 1.5];
freq  = freqs[(lastMarkerIdx) % freqs.length];
wiggle(freq, 30);
```

---

## 🌊 ADVANCED WIGGLE — ПРОДВИНУТЫЙ ВИГЛ

> wiggle() — это просто начало. Вот что можно с ним сделать по-настоящему.

### Wiggle только по одной оси с seed

```javascript
// Полностью независимые шумы для X и Y с разными seed:
t = time;
seedRandom(1, false);  // false = seed меняется со временем
wx = wiggle(1, 50)[0];

seedRandom(2, false);
wy = wiggle(1, 50)[1];

[value[0] + wx, value[1] + wy];
// Оси абсолютно независимы — органичнее чем стандартный wiggle
```

### Wiggle с затуханием (в начале сильный, потом гаснет)

```javascript
decayRate = 1.5;  // скорость затухания
envelope  = Math.exp(-decayRate * time);
w = wiggle(5, 60 * envelope);
[value[0] + w[0], value[1] + w[1]];
// В начале трясёт сильно, потом успокаивается
```

### Wiggle с нарастанием (в начале тихо, потом разгоняется)

```javascript
growthRate = 0.5;
envelope   = 1 - Math.exp(-growthRate * time);
w = wiggle(4, 50 * envelope);
[value[0] + w[0], value[1] + w[1]];
```

### Wiggle только в зоне (не выходит за границы)

```javascript
// Объект wiggle-ится, но не выходит за заданный прямоугольник
centerX = 960;
centerY = 540;
limitX  = 200;
limitY  = 100;

w = wiggle(2, 150);
x = clamp(w[0], centerX - limitX, centerX + limitX);
y = clamp(w[1], centerY - limitY, centerY + limitY);
[x, y];
```

### Directional wiggle — только вдоль оси движения

```javascript
// Трясётся в направлении движения (не перпендикулярно)
// Шаг 1: определяем направление движения:
dt     = thisComp.frameDuration;
posNow = transform.position.valueAtTime(time);
posPrev = transform.position.valueAtTime(time - dt);
dir    = sub(posNow, posPrev);
len    = length(dir);

if (len > 0.001) {
  normDir = normalize(dir);
} else {
  normDir = [1, 0];
}

// Шаг 2: wiggle вдоль направления:
w = wiggle(8, 15)[0];  // scalar wiggle
[value[0] + normDir[0] * w,
 value[1] + normDir[1] * w];
```

### Перпендикулярный wiggle (поперёк движения)

```javascript
dt      = thisComp.frameDuration;
posNow  = transform.position.valueAtTime(time);
posPrev = transform.position.valueAtTime(time - dt);
dir     = sub(posNow, posPrev);
len     = length(dir);

if (len > 0.001) {
  normDir = normalize(dir);
} else {
  normDir = [1, 0];
}
// Перпендикуляр: [-y, x]
perpDir = [-normDir[1], normDir[0]];

w = wiggle(6, 20)[0];
[value[0] + perpDir[0] * w,
 value[1] + perpDir[1] * w];
// Трясётся поперёк направления — как флаг на ветру
```

### Wiggle только когда объект движется

```javascript
dt       = thisComp.frameDuration;
posNow   = transform.position.valueAtTime(time);
posPrev  = transform.position.valueAtTime(time - dt);
velocity = length(sub(posNow, posPrev)) / dt;  // px/sec

// Амплитуда wiggle пропорциональна скорости:
wAmp = ease(velocity, 0, 500, 0, 30);
w    = wiggle(10, wAmp);
[value[0] + w[0], value[1] + w[1]];
```

### Double wiggle — крупные движения + мелкая дрожь

```javascript
// Два wiggle с разными масштабами — органичное движение
bigW   = wiggle(0.3, 80);   // редкие большие движения
smallW = wiggle(8, 5);       // частая мелкая дрожь
[value[0] + bigW[0] + smallW[0],
 value[1] + bigW[1] + smallW[1]];
```

### Wiggle с возвратом в ноль (mean-zero guarantee)

```javascript
// wiggle() имеет дрейф — уходит от нуля.
// Фикс: вычитаем медленный drift:
w      = wiggle(3, 40);
drift  = wiggle(0.1, 40);  // очень медленный — примерно равен среднему
[value[0] + w[0] - drift[0],
 value[1] + w[1] - drift[1]];
// Приблизительно симметрично вокруг оригинала
```

### Wiggle в полярных координатах (круговое дрожание)

```javascript
// Объект дрожит по радиусу и углу — не по X/Y
baseR   = 200;
baseA   = 0;

wr = wiggle(4, 30)[0];   // радиус дрожит
wa = wiggle(4, 15)[1];   // угол дрожит (в градусах)

r  = baseR + wr;
a  = (baseA + wa) * Math.PI / 180;

cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(a) * r,
 cy + Math.sin(a) * r];
```

### Wiggle под BPM (синхронизированный шум)

```javascript
// Шум "сбрасывается" каждые N бит — ощущение синхронности
bpm        = 120;
beatsPerCycle = 4;  // раз в 4 бита новый паттерн
secPerCycle = (60 / bpm) * beatsPerCycle;

// Время внутри цикла (0..secPerCycle):
cycleTime = time % secPerCycle;
// Семя меняется каждый цикл:
cycleSeed = Math.floor(time / secPerCycle);

seedRandom(cycleSeed * 100 + index, false);
// Wiggle с этим seed:
wiggle(2, 50);
// Каждые 4 бита шум получает новый паттерн — ощущение структуры
```

---

## 🎨 GRADIENT & COLOR ADVANCED — ЦВЕТ ПРОДВИНУТЫЙ

> Цвет в AE — это [R, G, B, A] от 0 до 1. Но это только начало.

### HSL -> RGB конвертация (менять оттенок без потери насыщенности)

```javascript
// AE работает в RGB, но управлять цветом удобнее в HSL
function hue2rgb(p, q, t) {
  if (t < 0) t += 1;
  if (t > 1) t -= 1;
  if (t < 1/6) return p + (q - p) * 6 * t;
  if (t < 1/2) return q;
  if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
  return p;
}
function hsl2rgb(h, s, l) {
  if (s === 0) return [l, l, l, 1];
  q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  p = 2 * l - q;
  return [hue2rgb(p, q, h + 1/3),
          hue2rgb(p, q, h),
          hue2rgb(p, q, h - 1/3),
          1];
}

// Оттенок крутится под бит:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
hue = (time * 0.1 + ease(amp, 0, 20, 0, 0.3)) % 1;  // 0..1
hsl2rgb(hue, 0.9, 0.5);
// Яркий насыщенный цвет, оттенок меняется со временем + прыгает на бит
```

### RGB -> HSL (чтение текущего цвета)

```javascript
function rgb2hsl(r, g, b) {
  max_ = Math.max(r, g, b);
  min_ = Math.min(r, g, b);
  l    = (max_ + min_) / 2;
  if (max_ === min_) return [0, 0, l];
  d = max_ - min_;
  s = l > 0.5 ? d / (2 - max_ - min_) : d / (max_ + min_);
  if (max_ === r) h = (g - b) / d + (g < b ? 6 : 0);
  else if (max_ === g) h = (b - r) / d + 2;
  else h = (r - g) / d + 4;
  return [h / 6, s, l];
}
```

### Lerp между двумя цветами под бит

```javascript
colorA = [0.1, 0.1, 0.9, 1];  // тёмно-синий
colorB = [1.0, 0.3, 0.1, 1];  // ярко-красный

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
t   = ease(amp, 0, 20, 0, 1);

r = colorA[0] + (colorB[0] - colorA[0]) * t;
g = colorA[1] + (colorB[1] - colorA[1]) * t;
b = colorA[2] + (colorB[2] - colorA[2]) * t;
[r, g, b, 1];
```

### Palette cycling — цвет переключается между N цветами

```javascript
palette = [
  [0.95, 0.1,  0.1,  1],
  [0.1,  0.7,  1.0,  1],
  [0.1,  0.95, 0.3,  1],
  [1.0,  0.85, 0.05, 1],
  [0.7,  0.1,  1.0,  1],
];
cycleDur = 1.0;  // секунд на каждый цвет
n        = palette.length;
idx      = Math.floor(time / cycleDur) % n;
palette[idx];
```

### Плавный переход между цветами палитры

```javascript
palette = [
  [0.95, 0.1,  0.1,  1],
  [0.1,  0.7,  1.0,  1],
  [0.1,  0.95, 0.3,  1],
  [1.0,  0.85, 0.05, 1],
];
cycleDur = 1.5;
n        = palette.length;
t        = (time / cycleDur) % n;
idxA     = Math.floor(t) % n;
idxB     = (idxA + 1) % n;
frac     = t - Math.floor(t);
st       = frac * frac * (3 - 2 * frac);  // smoothstep

cA = palette[idxA];
cB = palette[idxB];
[cA[0] + (cB[0]-cA[0]) * st,
 cA[1] + (cB[1]-cA[1]) * st,
 cA[2] + (cB[2]-cA[2]) * st,
 1];
```

### Температура цвета под бит (холодный -> тёплый)

```javascript
// Холодный (синий) в тишине, тёплый (оранжевый) на ударе
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
t   = ease(amp, 0, 20, 0, 1);

cold = [0.4, 0.6, 1.0];   // холодный синеватый
warm = [1.0, 0.5, 0.1];   // тёплый оранжевый
r = cold[0] + (warm[0] - cold[0]) * t;
g = cold[1] + (warm[1] - cold[1]) * t;
b = cold[2] + (warm[2] - cold[2]) * t;
[r, g, b, 1];
```

### Цвет зависит от position (градиент по экрану)

```javascript
// Слой меняет цвет в зависимости от X-позиции на экране
pos = transform.position;
t   = clamp(pos[0] / thisComp.width, 0, 1);

colorL = [1.0, 0.1, 0.3, 1];  // левый край — красный
colorR = [0.1, 0.3, 1.0, 1];  // правый край — синий

st = t * t * (3 - 2 * t);
[colorL[0] + (colorR[0]-colorL[0]) * st,
 colorL[1] + (colorR[1]-colorL[1]) * st,
 colorL[2] + (colorR[2]-colorL[2]) * st,
 1];
```

### Strobe — чередование двух цветов на ударе

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

colorA = [1.0, 1.0, 1.0, 1];  // белый
colorB = [0.0, 0.0, 0.0, 1];  // чёрный

fps   = thisComp.frameRate;
frame = Math.floor(time * fps);
// Стробоскоп активируется только на ударе:
if (amp > 15) {
  frame % 2 === 0 ? colorA : colorB;
} else {
  colorA;
}
```

### Saturation управление без effect (через RGB)

```javascript
// Обесцвечивание / насыщение вычислением
// Входной цвет из другого слоя или кейфрейма:
inputR = 0.8;
inputG = 0.3;
inputB = 0.1;
// Яркость (luminance):
lum = 0.299 * inputR + 0.587 * inputG + 0.114 * inputB;

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
saturation = ease(amp, 0, 20, 0, 1);  // 0 = серый, 1 = полный цвет

r = lum + (inputR - lum) * saturation;
g = lum + (inputG - lum) * saturation;
b = lum + (inputB - lum) * saturation;
[r, g, b, 1];
```

---

## 🪆 PARENTING & NULL TRICKS — НУЛЛЫ И ПЭРЕНТИНГ

> Нулл — это не просто "родитель". Это точка сборки всего рига.

### Получить абсолютную позицию дочернего слоя

```javascript
// Если нужна позиция в comp-координатах, а не локальных:
thisLayer.toComp([0, 0, 0]);
// Возвращает [x, y, z] в координатах компа — независимо от пэрента
```

### Конвертировать позицию между слоями

```javascript
// Позиция слоя A в координатах слоя B:
layerA = thisComp.layer("Object_A");
layerB = thisComp.layer("Object_B");

// Точка в компе из слоя A:
compPt = layerA.toComp(layerA.transform.anchorPoint);
// Эта точка в локальных координатах слоя B:
layerB.fromComp(compPt);
```

### Null как "виртуальная камера" (controller)

```javascript
// Null "CTRL" управляет позицией группы слоёв
// Слой-ребёнок: Position смещается ОТНОСИТЕЛЬНО нулла + своей орбиты:
ctrl = thisComp.layer("CTRL");
ctrlPos = ctrl.transform.position;

seedRandom(index * 61, true);
orbitR = random(50, 150);
orbitSpeed = random(0.2, 0.8);
orbitPhase = random(0, Math.PI * 2);

ox = Math.cos(time * orbitSpeed * Math.PI * 2 + orbitPhase) * orbitR;
oy = Math.sin(time * orbitSpeed * Math.PI * 2 + orbitPhase) * orbitR;
[ctrlPos[0] + ox, ctrlPos[1] + oy];
```

### Null — multiple inheritance (два родителя одновременно)

```javascript
// AE позволяет только одного Parent.
// Через expression — можно усреднить два нулла:
nullA = thisComp.layer("NULL_A");
nullB = thisComp.layer("NULL_B");
weight = 0.5;  // 0 = только A, 1 = только B
posA = nullA.transform.position;
posB = nullB.transform.position;
[posA[0] + (posB[0] - posA[0]) * weight,
 posA[1] + (posB[1] - posA[1]) * weight];
// Слой "между" двумя нуллами. weight = 0.5 -> ровно посередине.
```

### Null — привязка к вершине шейп-слоя

```javascript
// Получить позицию первой точки пути в comp-координатах:
shapeLayer = thisComp.layer("My Shape");
// Вершины пути через expression не читаются напрямую.
// Workaround: используй Effect -> CC Composite или Motion Path
// Реальный workaround: ставь Null через Snap to path в AE вручную,
// или используй createPath() в ExtendScript (не expression)
```

### Счётчик дочерних слоёв (сколько слоёв у этого пэрента)

```javascript
// Считаем слои с одним пэрентом:
myIndex   = index;
childCount = 0;
for (i = 1; i <= thisComp.numLayers; i++) {
  lay = thisComp.layer(i);
  // Проверяем parent через try/catch:
  try {
    if (lay.parent && lay.parent.index === myIndex) {
      childCount++;
    }
  } catch(e) {}
}
childCount;
// На Source Text нулла: показывает число дочерних слоёв
```

### Dynamic parenting — слой переключает пэрента в разное время

```javascript
// Нельзя менять Parent через expression напрямую.
// Workaround через Position: вычисляй позицию как будто ты привязан к разным нуллам:
nullA = thisComp.layer("NULL_A");
nullB = thisComp.layer("NULL_B");

switchTime = 2.0;  // секунд когда переключаемся
blendDur   = 0.3;  // длительность перехода

if (time < switchTime) {
  nullA.transform.position;
} else if (time < switchTime + blendDur) {
  t  = (time - switchTime) / blendDur;
  st = t * t * (3 - 2 * t);
  posA = nullA.transform.position;
  posB = nullB.transform.position;
  [posA[0] + (posB[0]-posA[0]) * st,
   posA[1] + (posB[1]-posA[1]) * st];
} else {
  nullB.transform.position;
}
```

---

## 💥 VFX SNIPPETS — ГОТОВЫЕ VFX СНИППЕТЫ

> Конкретные задачи — конкретный код. Копируй, вставляй, подстраивай.

### Мигалка (strobe light эффект) — Opacity

```javascript
// Частота мигания под бит:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
freq    = ease(amp, 0, 20, 2, 24);  // 2..24 Hz
fps     = thisComp.frameRate;
frame   = Math.floor(time * fps);
strobeOn = Math.floor(time * freq) % 2;
amp > 8 ? strobeOn * 100 : 100;
// Мигает только когда достаточно громко
```

### Аберрация хроматическая (через Position на дублях)

```javascript
// На R-копии слоя -> Position:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ca  = ease(amp, 0, 20, 0, 12);
[value[0] - ca, value[1] - ca * 0.3];

// На B-копии:
// [value[0] + ca, value[1] + ca * 0.3]
// G-копия остаётся на месте
```

### VHS-эффект (горизонтальный сдвиг случайных строк)

```javascript
// На Position слоя с footage + Offset effect или Displacement:
// Через Wave Warp effect -> Position X expression:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
fps = thisComp.frameRate;
frame = Math.floor(time * fps);
seedRandom(frame * 7 + index, true);
// Случайный горизонтальный сдвиг (срабатывает редко):
if (random(0, 1) > 0.95 || amp > 18) {
  random(-20, 20);
} else {
  0;
}
// Вешай на Turbulent Displace -> Amount или Wave Warp
```

### Glitch position (случайные прыжки кадрами)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
fps = thisComp.frameRate;
frame = Math.floor(time * fps);
seedRandom(frame * 13, true);

if (amp > 20 && random(0, 1) > 0.6) {
  // На ударе случайный прыжок:
  ox = random(-30, 30);
  oy = random(-15, 15);
} else {
  ox = 0;
  oy = 0;
}
[value[0] + ox, value[1] + oy];
```

### Пиксель-арт эффект (через Scale + Mosaic)

```javascript
// На Mosaic effect -> Horizontal Blocks:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// В тишине — мелкие пиксели (много блоков), на ударе — чёткий:
Math.round(ease(amp, 0, 20, 5, 200));
// Vertical Blocks: то же самое
```

### Zoom burst на удар (Scale от 100% до 500% мгновенно)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Резкий взрыв — используем easeOut для быстрой атаки:
s = easeOut(amp, 0, 20, 100, 500);
[s, s];
// Вешай на слой с footage + Mode = Add или Screen
// Создаёт вспышку zoom burst на каждый удар
```

### Echo trail — позиция с задержкой (ghost)

```javascript
// N дублей слоя, каждый на своей задержке:
delay = (index - 1) * 0.05;  // 50ms между каждым дублем
// На Position каждого дубля:
thisComp.layer("Original").transform.position.valueAtTime(time - delay);
// На Opacity каждого дубля:
// 100 - (index - 1) * 20;  // каждый следующий прозрачнее
```

### Scan line (бегущая полоса) — Position Y

```javascript
// Shape Layer (горизонтальная линия) бежит по экрану:
speed = thisComp.height / 2;  // px/sec — 2 секунды на экран
y = (time * speed) % (thisComp.height + 20) - 10;
[thisComp.width / 2, y];
```

### Scan line с откликом на бит (ускоряется)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed = thisComp.height / 3;
beatBoost  = ease(amp, 0, 20, 0, thisComp.height);
// Интеграл переменной скорости — через delta:
value[1] + (baseSpeed + beatBoost) * thisComp.frameDuration;
// ⚠️ Нужен стартовый кейфрейм на Y = -10
```

### Particle burst (N слоёв разлетаются от центра)

```javascript
// На каждом "частичном" слое -> Position:
// Угол полёта уникален для каждого слоя:
n       = 12;  // количество частиц
angle   = ((index - 1) / n) * Math.PI * 2;
// Скорость:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Частица вылетает при ударе:
speed  = easeOut(amp, 0, 20, 0, 400);  // px/sec
radius = speed * time;

cx = thisComp.width  / 2;
cy = thisComp.height / 2;
[cx + Math.cos(angle) * radius,
 cy + Math.sin(angle) * radius];
```

### TV static (шум на весь экран) — Fractal Noise Evolution

```javascript
// На Fractal Noise -> Evolution:
fps   = thisComp.frameRate;
frame = Math.floor(time * fps);
seedRandom(frame, true);
// Случайный evolution каждый кадр = чистый static:
random(0, 360 * 100);  // большой диапазон = полный рандом
```

### Shake с разной интенсивностью по осям (earthquake)

```javascript
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
// Вертикальное трясение сильнее горизонтального (как при взрыве):
shakeX = ease(amp, 0, 20, 0, 15);
shakeY = ease(amp, 0, 20, 0, 35);
freqX  = 18;
freqY  = 22;
ox = Math.sin(time * freqX * 6.28) * shakeX + wiggle(freqX * 0.5, shakeX * 0.3)[0];
oy = Math.sin(time * freqY * 6.28) * shakeY + wiggle(freqY * 0.5, shakeY * 0.3)[1];
[value[0] + ox, value[1] + oy];
```

### Typewriter эффект — знаки появляются по одному (Source Text)

```javascript
fullText  = "ПОСЛЕ УДАРА МИР ИЗМЕНИЛСЯ";
charsPerSec = 12;  // скорость печати
charsToShow = Math.floor(time * charsPerSec);
fullText.substring(0, Math.min(charsToShow, fullText.length));
```

### Typewriter с паузами на словах

```javascript
words    = ["BEAT", " IS ", "EVERYTHING"];
durations = [1.0, 0.5, 2.0];  // сек на каждое слово

result = "";
t = time;
for (i = 0; i < words.length; i++) {
  if (t > 0) {
    if (t >= durations[i]) {
      result += words[i];
      t -= durations[i];
    } else {
      // Частично показываем текущее слово:
      charsToShow = Math.floor((t / durations[i]) * words[i].length);
      result += words[i].substring(0, charsToShow);
      t = 0;
    }
  }
}
result;
```

---

## 🔌 EXPRESSION TO EXPRESSION — ЦЕПОЧКИ

> Один expression читает другой. Иерархии управления без единого кейфрейма.

### Slider читает Slider (цепочка обработки)

```javascript
// STAGE 1: [Layer "INPUT"] -> Slider "Raw Signal"
// Expression:
audioLayer = thisComp.layer("Audio Amplitude");
audioLayer.effect("Both Channels")("Slider");

// STAGE 2: [Layer "PROCESS"] -> Slider "Smoothed"
// Expression:
raw = thisComp.layer("INPUT").effect("Raw Signal")("Slider");
ease(raw, 0, 20, 0, 100);

// STAGE 3: [Layer "PROCESS"] -> Slider "Inverted"
// Expression:
smooth = thisLayer.effect("Smoothed")("Slider");
100 - smooth;

// STAGE 4: рабочий слой читает PROCESS:
proc = thisComp.layer("PROCESS");
s = proc.effect("Smoothed")("Slider");
ease(s, 0, 100, 100, 180);
[s, s];
```

### Арифметические цепочки

```javascript
// Умножитель — отдельный Slider "Multiplier" = 2.5
// Offset — отдельный Slider "Offset" = 30

M = thisComp.layer("MASTER");
raw   = M.effect("Beat Raw")("Slider");
mult  = M.effect("Multiplier")("Slider");
offs  = M.effect("Offset")("Slider");
clamp(raw * mult + offs, 0, 100);
```

### Conditional routing — разные входы в зависимости от чекбокса

```javascript
M = thisComp.layer("MASTER");
useBeat = M.effect("Use Beat")("Checkbox");
useProc = M.effect("Use Proc")("Checkbox");

beatVal = M.effect("Beat Smooth")("Slider");
procVal = M.effect("Proc Wave")("Slider");

if (useBeat && useProc) {
  (beatVal + procVal) / 2;  // микс
} else if (useBeat) {
  beatVal;
} else if (useProc) {
  procVal;
} else {
  50;  // дефолт
}
```

### Максимум из нескольких источников

```javascript
// Реагирует на самый сильный из нескольких сигналов:
M = thisComp.layer("MASTER");
beatVal = M.effect("Beat Smooth")("Slider");
procVal = M.effect("Proc Wave")("Slider");
waveVal = M.effect("Sin Wave")("Slider");
Math.max(beatVal, procVal, waveVal);
```

### Gate — сигнал проходит только если выше порога

```javascript
M   = thisComp.layer("MASTER");
sig = M.effect("Beat Smooth")("Slider");
thr = M.effect("Threshold")("Slider");  // значение порога из слайдера

if (sig > thr) {
  sig;
} else {
  0;
}
// Сигнал "открывается" только при превышении порога
```

### Компрессор (динамическое сжатие диапазона)

```javascript
M      = thisComp.layer("MASTER");
sig    = M.effect("Beat Raw")("Slider");
thresh = 10;   // порог компрессии
ratio  = 4;    // степень компрессии выше порога

if (sig <= thresh) {
  sig;
} else {
  thresh + (sig - thresh) / ratio;
}
// Тихие удары — без изменений, громкие — сжимаются
```

---

## 📊 DATA DRIVEN — ДАННЫЕ В АНИМАЦИЮ

> Массивы данных прямо в expression — никакого плагина.

### Анимация из массива значений (keyframe-free)

```javascript
// Данные прямо в выражении:
data = [100, 150, 80, 200, 120, 90, 180, 110, 160, 140];
dur  = 0.5;  // секунд на каждое значение
n    = data.length;
t    = (time / dur) % n;
idx  = Math.floor(t);
frac = t - idx;
st   = frac * frac * (3 - 2 * frac);  // smoothstep

// Lerp между текущим и следующим значением:
v1 = data[idx % n];
v2 = data[(idx + 1) % n];
s  = v1 + (v2 - v1) * st;
[s, s];
```

### Bar chart из массива (высота столбца по index)

```javascript
// Каждый Shape Layer = один столбец графика:
data = [45, 78, 23, 90, 56, 67, 34, 82, 15, 95];
idx  = (index - 1) % data.length;

// Анимированное появление столбца:
appearDur = 0.5;
stagger   = (index - 1) * 0.08;
t = clamp((time - stagger) / appearDur, 0, 1);
st = t * t * (3 - 2 * t);

height = data[idx] * 3;  // масштабируем: 1 единица = 3px
[50, height * st];  // [ширина, высота]
// Вешай на Rectangle Path -> Size
```

### Bar chart + beat: столбец дёргается под удар

```javascript
data = [45, 78, 23, 90, 56, 67, 34, 82];
idx  = (index - 1) % data.length;
baseH = data[idx] * 3;

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
beatBoost = ease(amp, 0, 20, 0, 30);

// Уникальная реакция каждого столбца:
seedRandom(index * 41, true);
myBoost = beatBoost * random(0.5, 1.5);

[50, baseH + myBoost];
```

### Анимация из строки (morse code через текст)

```javascript
// Кодируем паттерн как строку: "1" = on, "0" = off, " " = пауза
pattern  = "1 0 1 1 0 0 1 0 1";
elements = pattern.split(" ");
dur      = 0.2;  // секунд на символ
n        = elements.length;
t        = time % (n * dur);
idx      = Math.floor(t / dur);
elements[idx % n] === "1" ? 100 : 0;
// Opacity мигает по паттерну
```

### Таблица данных (2D массив)

```javascript
// Таблица: строки = категории, столбцы = временные шаги
table = [
  [10, 20, 40, 80, 60, 30],  // категория 1
  [80, 60, 30, 10, 40, 70],  // категория 2
  [30, 50, 70, 40, 20, 90],  // категория 3
];
rowDur  = 2.0;  // секунд на строку
colDur  = rowDur / table[0].length;

row = Math.floor(time / rowDur) % table.length;
col = Math.floor((time % rowDur) / colDur) % table[0].length;
val = table[row][col];

s = ease(val, 0, 100, 50, 200);
[s, s];
```

---

## 🏃 MOTION DESIGN PATTERNS — ПАТТЕРНЫ MOTION

> Классические MoGraph-паттерны через expressions. Без плагинов.

### Anticipation + action (замах перед действием)

```javascript
// Классика Disney: перед движением вперёд — маленький откат назад
// На Position Y:
actionTime  = 1.0;    // момент действия
anticipation = 0.15;  // секунд замаха
antAmp       = 20;    // px замаха
actionAmp    = -100;  // px действия

if (time < actionTime - anticipation) {
  value[1];
} else if (time < actionTime) {
  // Замах:
  t  = (time - (actionTime - anticipation)) / anticipation;
  st = t * t * (3 - 2 * t);
  value[1] + st * antAmp;
} else {
  // Действие:
  t  = time - actionTime;
  decay = Math.exp(-3 * t);
  value[1] + antAmp * decay + actionAmp * (1 - Math.exp(-8 * t));
}
```

### Overshoot (пролёт мимо цели с возвратом)

```javascript
// Объект летит к цели, проскакивает, возвращается
targetY   = 300;
startY    = value[1];
startTime = 0.5;   // когда начинает двигаться
duration  = 0.8;   // длительность движения

t = clamp((time - startTime) / duration, 0, 1);
// Overshoot curve: перелёт на 25% выше цели
overshoot = t < 0.7
  ? ease(t / 0.7, 0, 1, startY, targetY - (targetY - startY) * 0.25)
  : ease((t - 0.7) / 0.3, 0, 1, targetY - (targetY - startY) * 0.25, targetY);
[value[0], overshoot];
```

### Follow-through (инерция после остановки)

```javascript
// Продолжает двигаться после того как основная часть остановилась
// Хвост, волосы, детали
delay    = 0.2;   // отставание
damping  = 0.6;   // насколько меньше двигается хвост (0..1)

leader = thisComp.layer("Body");
mainPos = leader.transform.position;
delayedPos = leader.transform.position.valueAtTime(time - delay);

// Хвост = интерполяция между текущим и задержанным:
[mainPos[0] + (delayedPos[0] - mainPos[0]) * damping,
 mainPos[1] + (delayedPos[1] - mainPos[1]) * damping];
```

### Secondary animation (дополнительное движение детали)

```javascript
// Деталь (ухо, антенна) добавляет своё движение поверх родительского
// Без expression на родителе, только на ребёнке:
delay   = 0.12;
parent_ = thisComp.layer("Head");
// Вычитаем задержанную позицию родителя из текущей -> скорость:
posNow    = parent_.transform.position;
posDelayed = parent_.transform.position.valueAtTime(time - delay);
velX = (posNow[0] - posDelayed[0]) * 1.5;  // усиливаем
velY = (posNow[1] - posDelayed[1]) * 1.5;
// Добавляем к своей позиции:
[value[0] + velX, value[1] + velY];
```

### Ease in + hold + ease out (классический timing)

```javascript
// 3 фазы: плавный вход, удержание, плавный выход
inDur    = 0.5;
holdDur  = 1.0;
outDur   = 0.5;
total    = inDur + holdDur + outDur;
valStart = 0;
valHold  = 100;
valEnd   = 0;

t = time % total;  // зациклим для примера

if (t < inDur) {
  f = t / inDur;
  st = f * f * (3 - 2 * f);
  valStart + (valHold - valStart) * st;
} else if (t < inDur + holdDur) {
  valHold;
} else {
  f = (t - inDur - holdDur) / outDur;
  st = f * f * (3 - 2 * f);
  valHold + (valEnd - valHold) * st;
}
```

### Stutter motion (рывковое движение под бит)

```javascript
// Движение идёт "рывками" — hold, резкий шаг, hold
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
fps = thisComp.frameRate;

// Определяем "ударный" кадр:
frame     = Math.floor(time * fps);
isOnBeat  = amp > 18;

// Позиция обновляется только на ударных кадрах:
// (требует хранения состояния — обходим через seed по frame):
if (isOnBeat) {
  seedRandom(frame, true);
  targetX = random(-150, 150);
  targetY = random(-80, 80);
  [thisComp.width/2 + targetX, thisComp.height/2 + targetY];
} else {
  value;  // держим позицию
}
```

### Rubber band (резинка между двумя точками)

```javascript
// Объект тянется как резинка между двумя точками
pointA = thisComp.layer("Anchor_A").transform.position;
pointB = thisComp.layer("Anchor_B").transform.position;

// Параметрическая позиция вдоль резинки (t=0..1):
t = 0.5;  // середина (или из Slider)
// + провисание вниз:
midX = pointA[0] + (pointB[0] - pointA[0]) * t;
midY = pointA[1] + (pointB[1] - pointA[1]) * t;

// Провис (sag) пропорционален длине:
dist = length(pointA, pointB);
sag  = dist * 0.2;  // 20% от длины

[midX, midY + sag];
```

### MoGraph-клон: scale в шахматном порядке

```javascript
// Чётные столбцы и нечётные строки = инверсия
cols = 6;
col  = (index - 1) % cols;
row  = Math.floor((index - 1) / cols);

isEven = (col + row) % 2 === 0;

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");

if (isEven) {
  s = ease(amp, 0, 20, 100, 160);
} else {
  s = ease(amp, 0, 20, 100, 60);  // инверсия
}
[s, s];
// Шахматный паттерн масштаба
```

### Bounce grid (волна по 2D сетке)

```javascript
cols     = 6;
rows     = 5;
spacingX = 120;
spacingY = 100;

col = (index - 1) % cols;
row = Math.floor((index - 1) / cols);

// Расстояние от центра сетки:
centerCol = (cols - 1) / 2;
centerRow = (rows - 1) / 2;
distFromCenter = Math.sqrt(
  Math.pow(col - centerCol, 2) +
  Math.pow(row - centerRow, 2)
);

// Задержка по дистанции от центра:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
lag = distFromCenter * 0.08;
delayedAmp = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - lag);

s = ease(delayedAmp, 0, 20, 90, 160);

// Позиция в сетке + бит поднимает вверх:
startX = thisComp.width  / 2 - ((cols-1) * spacingX) / 2;
startY = thisComp.height / 2 - ((rows-1) * spacingY) / 2;
beatY  = ease(delayedAmp, 0, 20, 0, -40);

[startX + col * spacingX, startY + row * spacingY + beatY];
// Scale и Position одновременно реагируют — volюметрически
```

---

## ⚠️ TROUBLESHOOTING — ПОЛНОЕ РУКОВОДСТВО

> Здесь всё. От "не работает вообще" до тонких багов. Для новичков — с объяснением каждого шага.

---

### 🗂️ СОДЕРЖАНИЕ TROUBLESHOOTING

- [[#БЛОК 1 ПЕРВЫЙ ЗАПУСК — ничего не работает]]
- [[#БЛОК 2 ПРОИЗВОДИТЕЛЬНОСТЬ — AE лагает и тормозит]]
- [[#БЛОК 3 ОШИБКИ В EXPRESSION — красный текст]]
- [[#БЛОК 4 АУДИО — амплитуда не работает]]
- [[#БЛОК 5 СЛАЙДЕР КОНТРОЛ — как сделать и использовать]]
- [[#БЛОК 6 ЗНАЧЕНИЯ — неправильная реакция]]
- [[#БЛОК 7 POSITION И МАСШТАБ — слой прыгает или смещается]]
- [[#БЛОК 8 WIGGLE — непредсказуемое поведение]]
- [[#БЛОК 9 РАНДОМ — все объекты одинаковые]]
- [[#БЛОК 10 ВРЕМЯ — анимация не синхронизирована]]
- [[#БЛОК 11 3D И КАМЕРА — странное поведение в 3D]]
- [[#БЛОК 12 ТЕКСТ — Source Text не работает]]
- [[#БЛОК 13 SHAPE LAYERS — шейп не реагирует]]
- [[#БЛОК 14 ТОЛПА — все слои одинаковые]]
- [[#БЛОК 15 РЕНДЕР — в превью работает, в рендере нет]]
- [[#БЛОК 16 ДИАГНОСТИКА — как найти проблему самому]]

---

## БЛОК 1: ПЕРВЫЙ ЗАПУСК — ничего не работает

### Проблема: Написал expression, ничего не изменилось

```
ЧТО ПРОИСХОДИТ:
Expression написан, но свойство не реагирует. Слой стоит как стоял.

ПРИЧИНА 1: Expression не применён — ты написал текст, но не нажал Enter/галочку.

РЕШЕНИЕ:
1. Кликни на нужное свойство (Scale, Position, Opacity...)
2. Alt+Click (Win) / Option+Click (Mac) на иконку секундомера слева от свойства
3. Появится поле ввода с курсором
4. Введи expression
5. Нажми Enter на НУМПАДЕ или кликни в другое место
6. ⚠️ Обычный Enter делает перенос строки, НЕ применяет!
7. Если иконка секундомера стала ЖЁЛТОЙ — expression применён

КАК ПРОВЕРИТЬ ЧТО РАБОТАЕТ:
- Иконка секундомера = жёлтая (а не белая) -> expression активен
- Под свойством появился значок "fx" -> expression есть
- Значение свойства показывает вычисленный результат (может отличаться от 0)
```

### Проблема: Expression активен (жёлтый), но красным подчёркнут

```
ЧТО ПРОИСХОДИТ:
AE нашёл ошибку синтаксиса. Свойство замёрзло на последнем валидном значении.

РЕШЕНИЕ:
1. Кликни на красный текст expression в таймлайне
2. Откроется редактор с подсвеченной ошибкой
3. Смотри на описание ошибки внизу редактора
4. Чаще всего: опечатка, лишняя/пропущенная скобка, неверное имя

ЧАСТЫЕ ОШИБКИ СИНТАКСИСА:
// Было (ошибка — нет закрывающей скобки):
ease(amp, 0, 20, 100, 200;
// Надо:
ease(amp, 0, 20, 100, 200);

// Было (ошибка — русские кавычки):
thisComp.layer(«Audio Amplitude»);
// Надо (прямые кавычки):
thisComp.layer("Audio Amplitude");
```

### Проблема: Не знаю куда вообще писать expression

```
ШАГ ЗА ШАГОМ — как добавить expression на Scale:

1. Открой After Effects, создай комп с любым слоем
2. Выдели слой в таймлайне (клик на него)
3. Нажми S на клавиатуре — откроется Scale
4. Зажми Alt (Win) / Option (Mac) и кликни на ИКОНКУ СЕКУНДОМЕРА
   слева от слова "Scale"
5. В таймлайне появится поле ввода — это и есть expression editor
6. Напечатай: [100, 100]
7. Нажми Enter на нумпаде
8. Слой не изменился (100% — дефолт), но expression активен
9. Теперь напечатай: [150, 150]
10. Enter — слой стал 150%
11. Теперь попробуй: [100 + time * 10, 100 + time * 10]
12. Enter — слой растёт со временем

ГОТОВО. Это основа. Всё остальное — вариации этого.
```

---

## БЛОК 2: ПРОИЗВОДИТЕЛЬНОСТЬ — AE лагает и тормозит

### Проблема: AE зависает / лагает при воспроизведении

```
ПРИЧИНА: Много слоёв, каждый ходит к аудио-слою напрямую.

ПОЧЕМУ ЭТО ПЛОХО — объяснение для новичков:
Представь: у тебя 30 слоёв. На каждом expression лезет на слой
[Audio Amplitude] и читает значение. AE каждый кадр делает 30
отдельных обращений к аудио-данным. Это как 30 человек одновременно
открывают один и тот же тяжёлый файл с разных компов.

ПЛОХО (30 слоёв × прямая ссылка на аудио = 30 вычислений):
// На каждом из 30 слоёв:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 160);

ХОРОШО (1 вычисление, 30 слоёв читают результат):
// Шаг 1: Создай Null-слой (Layer -> New -> Null Object)
// Назови его "BEAT_MASTER"
//
// Шаг 2: Выдели Null "BEAT_MASTER"
// Effect -> Expression Controls -> Slider Control
// Появится эффект "Slider Control" в Effect Controls
// Переименуй его в "Beat" (двойной клик на названии)
//
// Шаг 3: На Null "BEAT_MASTER" -> Slider Control "Beat" -> Slider
// Alt+Click на секундомер -> вводи:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
//
// Шаг 4: На каждом рабочем слое -> Scale:
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat")("Slider");
mapped = ease(s, 0, 100, 100, 160);
[mapped, mapped];
//
// ИТОГ: AE считает аудио ОДИН раз (на Null),
// остальные 30 слоёв просто читают готовое число.
// Разница в скорости — в разы.
```

### Проблема: valueAtTime() тормозит

```
ПРИЧИНА: valueAtTime() — самая тяжёлая операция в expressions.
AE должен "перемотать" всю анимацию в указанный момент и вычислить.

РЕШЕНИЕ 1: Минимизировать количество вызовов
// Плохо — два вызова:
posNow  = transform.position.valueAtTime(time);
posPrev = transform.position.valueAtTime(time - 0.1);
// Хорошо — один вызов, второй берём из value:
posNow  = value;  // value = текущее, без лишнего вычисления
posPrev = transform.position.valueAtTime(time - 0.1);

РЕШЕНИЕ 2: Использовать Null-посредник
Если многие слои используют valueAtTime одного и того же слоя —
переложи это на Null, как описано выше.

РЕШЕНИЕ 3: Увеличить шаг задержки
// Вместо покадровой задержки:
valueAtTime(time - thisComp.frameDuration)  // каждый кадр = тяжело
// Используй фиксированную задержку:
valueAtTime(time - 0.1)  // 100ms — легче, выглядит так же
```

### Проблема: Большой проект с expressions рендерится медленно

```
ЧЕКЛИСТ ОПТИМИЗАЦИИ:

□ Все аудио-ссылки идут через один Null? (не напрямую)
□ Нет valueAtTime в цикле?
□ Нет бесконечных циклов (while без break)?
□ Сложные вычисления (sqrt, atan2) только там где нужно?
□ Отключены expressions на скрытых/невидимых слоях?
  (Layer -> Switches -> выключи "expressions" на неактивных)
□ Purge кэш перед рендером: Edit -> Purge -> All Memory and Disk Cache

РАДИКАЛЬНОЕ РЕШЕНИЕ для рендера:
1. Предварительно рендери comp с expressions в ProRes/DNxHD
2. Используй этот рендер как footage в финальном comp
3. Никаких expressions во время финального рендера
```

---

## БЛОК 3: ОШИБКИ В EXPRESSION — красный текст

### Как читать ошибки AE

```
ОТКУДА ЧИТАТЬ ОШИБКУ:
1. В таймлайне под слоем появляется красная строка с текстом ошибки
2. Или: открой Expression Editor (кликни на красный текст)
   В нижней части редактора — описание ошибки и номер строки

ТИПИЧНЫЕ ОШИБКИ И ЧТО ОНИ ЗНАЧАТ:

"Unable to execute script at line X"
-> Синтаксическая ошибка в строке X.
   Смотри: пропущена ли скобка, точка с запятой, кавычка.

"thisComp.layer: no layer with name Audio Amplitude"  
-> Слоя с таким именем нет в компе.
   Решение: проверь точное написание имени (регистр!).
   Или слой [Audio Amplitude] ещё не создан через Convert Audio to Keyframes.

"effect: no effect with name Both Channels"
-> Эффект называется по-другому (зависит от локализации AE).
   В русском AE: "Оба канала" вместо "Both Channels".
   Решение: кликни на слой [Audio Amplitude] -> смотри Effect Controls -> 
   запомни точные названия -> используй их в expression.

"Cannot read property 'value' of undefined"
-> Ты пытаешься читать свойство у объекта которого не существует.
   Например: layer("NAME") вернул null потому что слоя нет.

"Result must be of dimension X"
-> Ты вернул неправильный тип.
   Scale ожидает [x, y] (массив), ты вернул одно число.
   Решение: [s, s] вместо s.
```

### Проблема: Русскоязычный AE — эффекты называются по-русски

```
ПРИЧИНА: В русской локализации AE имена эффектов — по-русски.
Если в expression написано .effect("Both Channels") — AE не найдёт.

КАК УЗНАТЬ ТОЧНОЕ ИМЯ:
1. Выдели слой [Audio Amplitude]
2. Смотри в Effect Controls (Ctrl+5)
3. Там написано: "Оба канала", "Левый канал", "Правый канал"
4. Используй именно эти названия:
   audioLayer.effect("Оба канала")("Ползунок");
   //                ^^^^^^^^^^^^   ^^^^^^^^^^
   //                русское имя    "Slider" = "Ползунок" в русском AE

ЛАЙФХАК — переключи AE на английский:
1. Создай файл ae_force_english.txt в папке AE (или переключи в настройках)
2. Все имена станут английскими — expressions из интернета работают без изменений
3. Для CC 2019+: Edit -> Preferences -> General -> убери галку "Use System Language"
   (если есть такая опция, зависит от версии)

УНИВЕРСАЛЬНЫЙ СПОСОБ (работает на любом языке):
// Вместо имени эффекта — его индекс:
audioLayer.effect(1)("Slider");  // первый эффект на слое
// Но это ненадёжно если порядок эффектов меняется.
```

### Проблема: Expression работал, потом сломался после переименования слоя

```
ПРИЧИНА: thisComp.layer("ИМЯ") ищет слой по ИМЕНИ.
Переименовал слой -> все expressions которые на него ссылаются — сломались.

РЕШЕНИЕ 1: Выработай привычку — называй технические слои раз и навсегда
Имена которые никогда не меняй:
"Audio Amplitude" — стандартное имя от Convert Audio to Keyframes
"BEAT_MASTER"     — твой главный null
"PROC_MASTER"     — процедурный null
"CONTROLS"        — null с контролами

РЕШЕНИЕ 2: Ссылка через переменную в начале expression
// Если вдруг переименуешь — меняешь только одну строку:
masterNull = thisComp.layer("BEAT_MASTER");  // <-- только тут
beat = masterNull.effect("Beat")("Slider");
// ...остальной код не трогаешь

РЕШЕНИЕ 3: thisComp.layer(index) — по номеру, не по имени
// Ненадёжно (порядок слоёв меняется), используй только для быстрых тестов
thisComp.layer(1);  // первый слой в таймлайне
```

---

## БЛОК 4: АУДИО — амплитуда не работает

### Проблема: Слой [Audio Amplitude] отсутствует / нет кейфреймов

```
ЧТО ТАКОЕ [Audio Amplitude] — объяснение для новичков:
AE не умеет "слушать" аудио в реальном времени в expressions.
Вместо этого: ты один раз запускаешь инструмент который
КОНВЕРТИРУЕТ звук в кейфреймы — обычные числа на таймлайне.
Эти числа — и есть "амплитуда" которую читает expression.

КАК СОЗДАТЬ [Audio Amplitude]:
1. Убедись что в компе есть аудио-слой (импортируй MP3/WAV/AAC)
2. Кликни на аудио-слой в таймлайне (он должен быть выделен)
3. В меню: Animation -> Keyframe Assistant -> Convert Audio to Keyframes
   (русский AE: Анимация -> Помощник ключевого кадра -> Преобразовать аудио в ключевые кадры)
4. AE подумает несколько секунд
5. В таймлайне появится новый слой: [Audio Amplitude]
6. Разверни его: нажми стрелку слева от слоя
7. Там будет: Effects -> Both Channels, Left Channel, Right Channel
8. У каждого есть Slider с кейфреймами — это и есть амплитуда

⚠️ ЧАСТЫЕ ОШИБКИ:
- Запустил Convert Audio без выделения аудио-слоя -> ничего не создалось
- Аудио-слой замьючен (M) -> всё равно создаётся, это не мешает
- Аудио вне рабочей области (Work Area) -> создаётся только в пределах Work Area
  Решение: Composition -> Trim Comp to Work Area или расширь Work Area

ПРОВЕРКА ЧТО [Audio Amplitude] СОЗДАН ПРАВИЛЬНО:
1. Найди слой [Audio Amplitude] в таймлайне
2. Нажми U (показать анимированные свойства)
3. Должны появиться три дорожки со множеством кейфреймов
4. Нажми Space — слой должен "двигаться" (Slider меняет значения)
```

### Проблема: Амплитуда всегда 0 даже после Convert Audio to Keyframes

```
ПРИЧИНА 1: Аудио-слой был без аудио (видео без звука)
ПРОВЕРКА: 
- Правый клик на слой -> Reveal in Finder/Explorer
- Открой файл в плеере — есть ли звук?
- В AE: Window -> Audio -> должен двигаться индикатор при воспроизведении

ПРИЧИНА 2: Аудио слишком тихое
РЕШЕНИЕ:
- Подними громкость аудио-слоя: Layer -> Audio -> Audio Options
- Или в самом expression умножь amp * 5 или больше

ПРИЧИНА 3: Convert Audio был запущен без выделения аудио
РЕШЕНИЕ: Удали [Audio Amplitude], выдели аудио-слой, запусти снова

ПРИЧИНА 4: Expression ссылается на слой с неправильным именем
ДИАГНОСТИКА:
1. Кликни прямо на [Audio Amplitude] в таймлайне
2. Нажми Enter — слой переименовывается
3. Смотри ТОЧНОЕ имя (может быть пробел в конце, другой регистр)
4. Скопируй имя, вставь в expression в кавычки
```

### Проблема: Амплитуда есть, но реакция слишком слабая

```
ЧТО ПРОИСХОДИТ:
Разные треки имеют разную громкость.
Мастеред поп-трек: амплитуда 20-30 на ударах.
Тихий инди-трек: амплитуда 3-8 на ударах.
Твой tMax в ease() рассчитан не под этот трек.

КАК ОТКАЛИБРОВАТЬ:
1. Создай временный Text Layer
2. Вставь expression на Source Text:
   audioLayer = thisComp.layer("Audio Amplitude");
   amp = audioLayer.effect("Both Channels")("Slider");
   Math.round(amp * 10) / 10 + "";
3. Запусти воспроизведение — смотри числа в реальном времени
4. Запомни: какое число при тишине? какое на ударе?
5. Используй эти числа как tMin и tMax в ease():
   // Если тишина = 2, удар = 12:
   ease(amp, 2, 12, 100, 200);
6. Удали тестовый текстовый слой

БЫСТРЫЙ ФИКС без калибровки:
// Просто уменьши tMax вдвое:
ease(amp, 0, 10, 100, 200);  // было 20, стало 10 — реагирует вдвое сильнее
```

---

## БЛОК 5: СЛАЙДЕР КОНТРОЛ — как сделать и использовать

> Это самый важный блок для новичков. Slider Control = сердце любого рига.

### Что такое Slider Control и зачем он нужен

```
ОБЪЯСНЕНИЕ ДЛЯ НОВИЧКОВ:

Slider Control — это просто числовое поле которое:
1. Ты можешь анимировать кейфреймами
2. Другие expressions могут читать из него
3. Ты можешь крутить руками в реальном времени

ЗАЧЕМ:
Без Slider Control каждый слой сам вычисляет амплитуду.
30 слоёв = 30 вычислений каждый кадр = лаг.

Со Slider Control:
- Один Null считает амплитуду -> кладёт результат в Slider
- 30 слоёв читают Slider = 30 простых чтений числа
- AE работает в разы быстрее

АНАЛОГИЯ:
Slider Control = доска объявлений.
Один человек (Null) пишет на доске актуальную информацию.
30 человек (слои) просто смотрят на доску.
Без доски: каждый из 30 человек сам бы ходил за информацией.
```

### Пошаговая инструкция: создать Slider Control с нуля

```
ШАГ 1: Создай Null-объект
- Layer -> New -> Null Object
- Появится слой "Null 1" в таймлайне
- Двойной клик на название -> переименуй в "BEAT_MASTER"
- Enter для подтверждения

ШАГ 2: Добавь Slider Control на Null
- Выдели "BEAT_MASTER" в таймлайне
- Effect -> Expression Controls -> Slider Control
- В окне Effect Controls появится "Slider Control" с числом 0
- Двойной клик на "Slider Control" -> переименуй в "Beat"
- Enter

ШАГ 3: Поставь expression на Slider
- В таймлайне разверни BEAT_MASTER: нажми стрелку слева
- Разверни Effects -> Beat -> Slider
- Alt+Click на иконку секундомера слева от "Slider"
- Появится поле ввода
- Введи:
  audioLayer = thisComp.layer("Audio Amplitude");
  amp = audioLayer.effect("Both Channels")("Slider");
  ease(amp, 0, 20, 0, 100);
- Enter на нумпаде

ШАГ 4: Проверь что Slider работает
- Нажми Space — воспроизведи комп
- В Effect Controls BEAT_MASTER смотри на "Beat" Slider
- Он должен двигаться в такт музыке
- Если стоит на 0 — проверь что [Audio Amplitude] создан и назван правильно

ШАГ 5: Подключи рабочий слой к Slider
- Выдели рабочий слой (тот который должен реагировать)
- Нажми S -> разворачивается Scale
- Alt+Click на секундомер Scale
- Введи:
  null_ = thisComp.layer("BEAT_MASTER");
  s = null_.effect("Beat")("Slider");
  mapped = ease(s, 0, 100, 100, 150);
  [mapped, mapped];
- Enter на нумпаде
- Воспроизведи — слой должен реагировать!

ШАГ 6: Подключи остальные слои
- Повтори Шаг 5 для каждого слоя
- На каждом — только две строки меняются (что берём и как маппим):
  null_ = thisComp.layer("BEAT_MASTER");  // эта строка одинакова везде
  s = null_.effect("Beat")("Slider");      // эта тоже
  // дальше — под каждое свойство своё:
  ease(s, 0, 100, 0, 45);                 // для Rotation
  // или:
  ease(s, 0, 100, 100, 0);                // для инверсии
```

### Несколько Slider Control на одном Null

```
ЗАЧЕМ НЕСКОЛЬКО:
- "Beat Smooth" — плавный отклик (для scale, opacity)
- "Beat Sharp"  — резкий отклик (для ударных акцентов)
- "Beat Raw"    — сырой сигнал (для диагностики)
- "Energy"      — глобальная интенсивность (кейфреймируешь вручную)

КАК ДОБАВИТЬ ВТОРОЙ:
1. Выдели BEAT_MASTER
2. Effect -> Expression Controls -> Slider Control (снова)
3. Переименуй в "Beat Sharp"
4. Alt+Click на его Slider -> введи:
   audioLayer = thisComp.layer("Audio Amplitude");
   amp = audioLayer.effect("Both Channels")("Slider");
   easeOut(amp, 0, 20, 0, 100);  // easeOut = резче чем ease
5. Enter

ТЕПЕРЬ У ТЕБЯ ДВА СЛАЙДЕРА:
- "Beat"       -> ease()    -> плавный
- "Beat Sharp" -> easeOut() -> резкий

Используй нужный на каждом слое:
// Для нежного Scale (плавный):
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat")("Slider");
// Для резкого вспышки Opacity (резкий):
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Sharp")("Slider");
```

### Как читать Slider из другого слоя (пикер)

```
СПОСОБ 1: Вручную (как описано выше)
null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat")("Slider");

СПОСОБ 2: Через Expression Pick Whip (визуально, без текста)
1. Открой нужное свойство (например Scale) с expression полем
2. В поле expression есть иконка "спираль" (pick whip)
3. Зажми её и протяни к Slider Control на BEAT_MASTER
4. AE автоматически напишет правильную ссылку
5. После этого ты можешь руками дописать ease() вокруг:
   // AE написал что-то вроде:
   thisComp.layer("BEAT_MASTER").effect("Beat")("Slider")
   // Ты дописываешь:
   s = thisComp.layer("BEAT_MASTER").effect("Beat")("Slider");
   ease(s, 0, 100, 100, 160);
   [ease(s, 0, 100, 100, 160), ease(s, 0, 100, 100, 160)];
```

---

## БЛОК 6: ЗНАЧЕНИЯ — неправильная реакция

### Проблема: Слой реагирует слишком мало / совсем не реагирует

```
ДИАГНОСТИКА — шаг за шагом:

Шаг 1: Проверь что амплитуда вообще есть (см. Блок 4)

Шаг 2: Выведи амплитуду как текст
- Создай Text Layer
- Alt+Click на Source Text -> введи:
  audioLayer = thisComp.layer("Audio Amplitude");
  amp = audioLayer.effect("Both Channels")("Slider");
  "" + Math.round(amp);
- Воспроизведи — смотри числа. Например: 0, 1, 2, 8, 15, 3...
- Запомни максимальное число на ударах (допустим, 8)

Шаг 3: Откалибруй tMax
- Если максимум амплитуды = 8, а у тебя tMax = 20:
  ease(amp, 0, 20, 100, 200)  // при amp=8 это даёт ~150, но не максимум
- Исправь tMax под реальный максимум:
  ease(amp, 0, 8, 100, 200)   // теперь при amp=8 даёт полные 200

Шаг 4: Проверь что expression применён на нужное свойство
- Иконка секундомера должна быть ЖЁЛТОЙ (не белой)
- Если белая — expression не активен
```

### Проблема: Слой реагирует слишком сильно / вылетает за экран

```
ПРИЧИНА: tMax слишком маленький или valMax слишком большой.

РЕШЕНИЕ:
// Было (tMax=5 — реагирует уже при любом шуме):
ease(amp, 0, 5, 100, 500);
// Стало (tMax=20 — нужен реальный удар):
ease(amp, 0, 20, 100, 200);

// Или уменьши valMax:
ease(amp, 0, 20, 100, 130);  // максимум только +30% вместо +100%

// Или добавь clamp для жёсткого ограничения:
s = ease(amp, 0, 20, 100, 500);
s = clamp(s, 0, 200);  // никогда не выйдет за 200%
[s, s];
```

### Проблема: Значение плавает в тишине (не стоит на нуле)

```
ПРИЧИНА: Аудио-файл имеет фоновый шум, тишина = не 0 а 1-3.

РЕШЕНИЕ 1: Поднять tMin
// Было:
ease(amp, 0, 20, 100, 200);
// Стало (игнорируем всё до 3):
ease(amp, 3, 20, 100, 200);
// До 3 = будет давать 100 (valMin), не шевелится

РЕШЕНИЕ 2: Добавить gate (порог):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
gated = amp < 3 ? 0 : amp;  // всё до 3 = принудительно 0
ease(gated, 0, 20, 100, 200);
```

### Проблема: Значение прыгает резко без плавности

```
ПРИЧИНА: Используешь прямое умножение или linear() — нет смягчения.

ТАБЛИЦА ПЛАВНОСТИ (от жёсткого к мягкому):
amp * 5              -> максимально жёсткий, прямой
linear(amp, 0,20,x,y) -> линейный, без смягчения
easeIn(amp, 0,20,x,y) -> мягкий вход (атака), резкий выход
easeOut(amp,0,20,x,y) -> резкий вход (атака), мягкое затухание
ease(amp, 0,20,x,y)   -> мягко с обеих сторон

ВЫБОР ПОД ЗАДАЧУ:
- Ударные инструменты -> easeOut (резкий удар, мягкое затухание)
- Пэды, атмосфера     -> ease (всё плавно)
- Точный BPM sync     -> linear или easeOut
- Органичное дыхание  -> ease
```

### Проблема: Нужны и кейфреймы, и beat reaction

```
ПРИЧИНА/РЕШЕНИЕ:
Expression ПОЛНОСТЬЮ ЗАМЕНЯЕТ кейфреймы если стоит на свойстве.
Но можно сложить: кейфреймовое значение + beat добавка.

КАК:
// value — это текущее значение кейфреймов в данный момент
// К нему прибавляем beat реакцию:

// Для числового свойства (Opacity, Rotation, Slider):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
value + ease(amp, 0, 20, 0, 30);
// value = то что на кейфреймах, + до 30 единиц от бита

// Для Position (массив):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = ease(amp, 0, 20, 0, -50);
[value[0], value[1] + oy];
// Кейфреймовая позиция + прыжок вверх на бит

// Для Scale (массив):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
boost = ease(amp, 0, 20, 0, 30);
[value[0] + boost, value[1] + boost];
```

---

## БЛОК 7: POSITION И МАСШТАБ — слой прыгает или смещается

### Проблема: Слой прыгает в (0, 0) при добавлении expression на Position

```
ПРИЧИНА: Expression вернул неправильный тип.
Position ожидает массив [x, y].
Если вернуть одно число — слой прыгает в непонятное место.

ЧАСТАЯ ОШИБКА:
// НЕПРАВИЛЬНО — возвращает одно число:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp * 5;  // <- это одно число, не [x, y]!

// ПРАВИЛЬНО — возвращает массив:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = amp * 5;
[value[0], value[1] + oy];  // <- [x, y] с добавкой только по Y
```

### Проблема: Position expression работает, но слой не там где нужно

```
ПРИЧИНА: Забыл добавить value[] к базовой позиции.

// НЕПРАВИЛЬНО — слой телепортируется в абсолютные координаты:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = ease(amp, 0, 20, 0, -50);
[960, 540 + oy];  // <- хардкод координат = работает только на 1920x1080

// ПРАВИЛЬНО — смещение от текущей позиции слоя:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = ease(amp, 0, 20, 0, -50);
[value[0], value[1] + oy];  // <- value = текущая позиция из кейфреймов

// ПОЧЕМУ value ЛУЧШЕ:
// Если ты двигаешь слой руками или анимируешь кейфреймами —
// expression смещает его относительно ЭТОЙ позиции, а не абсолютно.
```

### Проблема: Scale работает, но трансформация идёт не от нужной точки

```
ПРИЧИНА: Anchor Point стоит не там где ты думаешь.

КАК ПРОВЕРИТЬ И ИСПРАВИТЬ:
1. Выдели слой
2. Нажми A -> открывается Anchor Point
3. Посмотри значение. По умолчанию AE ставит AP в центр слоя.
   Если слой 200x200px: AP должен быть [100, 100]
   Если AP = [0, 0] — трансформация идёт от верхнего левого угла

ИСПРАВЛЕНИЕ ЧЕРЕЗ EXPRESSION НА ANCHOR POINT:
r = sourceRectAtTime(time);
[r.left + r.width / 2, r.top + r.height / 2];
// Это всегда ставит AP в настоящий центр слоя

ДЛЯ ТРАНСФОРМАЦИИ ОТ НИЖНЕГО КРАЯ (текст растёт вверх):
r = sourceRectAtTime(time);
[r.left + r.width / 2, r.top + r.height];
// AP в нижнем центре — Scale растёт вверх

⚠️ ВАЖНО: Когда меняешь AP через expression — слой визуально прыгает!
Нужно компенсировать Position:
// Это делается через Layer -> Transform -> Auto-Orient
// Или вручную пересчитывая Position
```

### Проблема: 3D слой ведёт себя странно при Scale expression

```
ПРИЧИНА: 3D Scale = массив из ТРЁХ значений [x, y, z].

// НЕПРАВИЛЬНО для 3D слоя:
[s, s];     // только два значения!

// ПРАВИЛЬНО для 3D слоя:
[s, s, s];  // три значения

// КАК УЗНАТЬ 3D ЛИ СЛОЙ:
// В таймлайне у слоя есть иконка куба (3D Layer switch)
// Или: нажми P, S, R — Position покажет три координаты [x, y, z]
```

---

## БЛОК 8: WIGGLE — непредсказуемое поведение

### Проблема: Все слои wiggle-ятся одинаково (синхронно)

```
ПРИЧИНА: wiggle() автоматически использует index слоя как часть seed.
НО: если все слои созданы одновременно или скопированы — их index разный,
wiggle() ДОЛЖЕН быть разным. Если одинаковый — значит что-то не так.

ДИАГНОСТИКА:
// Добавь на Source Text тестового слоя:
index + "";
// Все слои должны показывать разные числа (1, 2, 3...)
// Если все = 1 — ты работаешь с Pre-comp и там один слой.

ПРИНУДИТЕЛЬНО РАЗНЫЕ ПАТТЕРНЫ:
seedRandom(index * 137, true);  // разный seed для каждого слоя
wiggle(2, 50);
// Теперь гарантированно разные, даже если index одинаковый
```

### Проблема: wiggle уходит далеко от оригинальной позиции (дрейф)

```
ПРИЧИНА: wiggle() — шум Перлина. Он не гарантирует возврат к нулю.
Со временем может дрейфовать в сторону.

РЕШЕНИЕ 1: Огранить clamp
w = wiggle(2, 100);
x = clamp(w[0], value[0] - 80, value[0] + 80);
y = clamp(w[1], value[1] - 80, value[1] + 80);
[x, y];

РЕШЕНИЕ 2: Вычесть медленный дрейф
w     = wiggle(2, 80);
drift = wiggle(0.05, 80);  // очень медленный = примерно равен среднему
[value[0] + w[0] - drift[0],
 value[1] + w[1] - drift[1]];

РЕШЕНИЕ 3: Использовать Math.sin вместо wiggle
// Sin гарантированно возвращается к нулю:
freq = 1.5;
amp_ = 50;
oy = Math.sin(time * freq * Math.PI * 2) * amp_;
[value[0], value[1] + oy];
```

### Проблема: wiggle не реагирует на изменение параметров в реальном времени

```
ПРИЧИНА: AE кэширует вычисления. При изменении expression параметров
иногда нужно очистить кэш.

РЕШЕНИЕ:
Edit -> Purge -> All Memory and Disk Cache
Или просто: Caps Lock -> снять Caps Lock
(это сбрасывает предпросмотр и пересчитывает)
```

---

## БЛОК 9: РАНДОМ — все объекты одинаковые

### Проблема: random() даёт одинаковое значение на всех слоях

```
ПРИЧИНА: random() без seedRandom() использует один seed для всех.

ПРАВИЛО:
Всегда добавляй seedRandom(index * PRIME, true) перед random().
PRIME — любое простое число: 7, 11, 13, 17, 23, 37, 41, 53, 61, 71, 97...

// НЕПРАВИЛЬНО (все слои получат одно число):
s = random(50, 150);
[s, s];

// ПРАВИЛЬНО (каждый слой своё):
seedRandom(index * 41, true);  // 41 — простое
s = random(50, 150);
[s, s];

ПОЧЕМУ ПРОСТОЕ ЧИСЛО:
random(50, 150) + seedRandom(index * 4, true):
  index=1: seed=4
  index=2: seed=8
  index=3: seed=12
  ...эти числа кратны друг другу, могут давать похожие паттерны

random(50, 150) + seedRandom(index * 41, true):
  index=1: seed=41
  index=2: seed=82
  index=3: seed=123
  ...числа более равномерно распределены по пространству seed
```

### Проблема: random() каждый кадр даёт разное значение (мигание)

```
ПРИЧИНА: random() без timeless=true меняется каждый кадр.

// МЕНЯЕТСЯ КАЖДЫЙ КАДР (если это не нужно):
seedRandom(index * 41, false);  // false = обновляется со временем
s = random(50, 150);

// ФИКСИРОВАНО ДЛЯ СЛОЯ (не меняется):
seedRandom(index * 41, true);   // true = фиксированный seed
s = random(50, 150);

// МЕНЯЕТСЯ КАЖДУЮ СЕКУНДУ (не каждый кадр):
fps     = thisComp.frameRate;
second  = Math.floor(time);
seedRandom(index * 41 + second * 100, true);
s = random(50, 150);
```

---

## БЛОК 10: ВРЕМЯ — анимация не синхронизирована

### Проблема: Синусоида не совпадает с ритмом музыки

```
ПРИЧИНА: Math.sin использует радианы, частота задана неправильно.

КАК ПРАВИЛЬНО ЗАДАВАТЬ ЧАСТОТУ:
freq = X  ->  X полных циклов в секунду (Гц)

// 1 Hz = 1 качок в секунду:
Math.sin(time * 1 * Math.PI * 2) * amp;

// 2 Hz = 2 качка в секунду:
Math.sin(time * 2 * Math.PI * 2) * amp;

// Под BPM 120 (2 удара в секунду):
bpm = 120;
freq = bpm / 60;  // = 2 Hz
Math.sin(time * freq * Math.PI * 2) * amp;

// Под BPM 120, раз в такт (4/4):
bpm = 120;
freq = bpm / 60 / 4;  // = 0.5 Hz — раз в 4 удара
Math.sin(time * freq * Math.PI * 2) * amp;
```

### Проблема: BPM sync сбивается со временем

```
ПРИЧИНА: time в AE начинается не с 0 если комп не с начала,
или аудио не синхронизировано с началом компа.

РЕШЕНИЕ 1: Убедись что аудио начинается на 0:00:00
- Потяни аудио-слой так чтобы его начало = начало таймлайна
- Или: Layer -> Time -> Time Stretch -> подгони

РЕШЕНИЕ 2: Добавь смещение в expression
bpmOffset = 0.05;  // подбирай пока не совпадёт
bpm = 120;
freq = bpm / 60;
Math.sin((time + bpmOffset) * freq * Math.PI * 2) * amp;

РЕШЕНИЕ 3: Использовать Convert Audio to Keyframes
Вместо математического BPM sync — пусть реальная амплитуда
управляет анимацией. Точнее любого BPM расчёта.
```

### Проблема: valueAtTime возвращает неожиданное значение

```
ПРИЧИНА: valueAtTime читает значение ПОСЛЕ вычисления всех expressions.
Это может создавать рекурсию если expression читает само себя.

БЕЗОПАСНОЕ ИСПОЛЬЗОВАНИЕ:
// Читать ДРУГОЙ слой — безопасно:
otherLayer.transform.position.valueAtTime(time - 0.2);

// Читать СЕБЯ с задержкой — осторожно!
// Если expression на Position читает Position самого себя:
transform.position.valueAtTime(time - 0.1);
// AE может зациклиться. Используй только если знаешь что делаешь.
// Более безопасно: читать через кейфреймы (без expression на свойстве).
```

---

## БЛОК 11: 3D И КАМЕРА — странное поведение в 3D

### Проблема: Expression на Position работает в 2D, но не в 3D

```
ПРИЧИНА: В 3D Position = [x, y, z] — три значения, не два.

// 2D:
[value[0] + ox, value[1] + oy];

// 3D:
[value[0] + ox, value[1] + oy, value[2]];
//                               ^^^^^^^^^ не забудь Z!

КАК УЗНАТЬ 3D ЛИ СЛОЙ:
- В таймлайне: иконка куба у слоя = 3D включён
- Нажми P на слое: если Position = три числа [x, y, z] — 3D
```

### Проблема: Camera expression не работает / камера не двигается

```
ПРИЧИНА 1: Нет 3D слоёв в компе — камера не влияет на 2D слои.
РЕШЕНИЕ: Включи 3D Layer switch (куб) хотя бы на одном слое.

ПРИЧИНА 2: Expression на Camera position возвращает 2D массив.
РЕШЕНИЕ: Camera Position всегда 3D:
[value[0] + ox, value[1] + oy, value[2]];  // Z оставляем из value

ПРИЧИНА 3: Несколько камер в компе — активна не та.
РЕШЕНИЕ: 
- Активная камера = та у которой нет глаза в колонке Solo
- Или: View -> Camera -> выбери нужную
- В expressions: thisComp.activeCamera — автоматически берёт активную
```

---

## БЛОК 12: ТЕКСТ — Source Text не работает

### Проблема: Source Text expression возвращает не текст а число

```
ПРИЧИНА: Source Text ожидает строку (string), а не число.

// НЕПРАВИЛЬНО (вернёт ошибку или пустоту):
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp;  // <- это число, не строка

// ПРАВИЛЬНО — конвертируй в строку через + "":
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
Math.round(amp) + "";  // <- число + пустая строка = строка

// Или через String():
String(Math.round(amp));
```

### Проблема: Текст обрезается / не помещается

```
ПРИЧИНА: Source Text меняет строку, но размер текстового бокса фиксирован.

РЕШЕНИЕ:
- Убедись что Text Layer в режиме "Point Text" (не Paragraph Text)
- Point Text растягивается автоматически
- Paragraph Text обрезает по рамке

КАК ПЕРЕКЛЮЧИТЬ:
Layer -> Layer Settings -> нет такой опции.
Прямо на тексте: двойной клик -> инструмент текста активен ->
в Character/Paragraph панели переключи тип.
Или пересоздай текстовый слой: Layer -> New -> Text.
```

---

## БЛОК 13: SHAPE LAYERS — шейп не реагирует

### Проблема: Expression на Size шейпа не работает

```
ПРИЧИНА: Путь до свойства Size отличается для разных типов шейпов.

Rectangle:
Contents -> "Rectangle 1" -> "Rectangle Path 1" -> Size

Ellipse:
Contents -> "Ellipse 1" -> "Ellipse Path 1" -> Size

Polystar:
Contents -> "Polystar 1" -> "Polystar Path 1" -> Points (не Size!)
Contents -> "Polystar 1" -> "Polystar Path 1" -> Outer Radius

КАК НАЙТИ ПРАВИЛЬНЫЙ ПУТЬ:
1. Разверни Shape Layer в таймлайне (стрелка)
2. Разверни Contents
3. Разворачивай вложенные группы пока не найдёшь нужное свойство
4. Alt+Click на секундомер именно того свойства

⚠️ ЧАСТАЯ ОШИБКА: Expression поставлен на Scale слоя,
а не на Size внутри шейпа. Scale = трансформация ВСЕГО слоя.
Size внутри пути = изменение самой формы. Разные вещи!
```

### Проблема: Trim Paths не рисует

```
ПРИЧИНА: Trim Paths ищется в конкретной группе, а может быть не там.

ПУТЬ ДО TRIM PATHS:
Contents -> [Группа] -> Trim Paths -> End (или Start)

⚠️ Trim Paths должен быть ВНУТРИ той же группы что и Path.
Если Trim Paths снаружи группы — он не влияет на путь внутри.

КАК ДОБАВИТЬ ПРАВИЛЬНО:
1. Разверни Shape Layer
2. Выдели нужную группу (клик на "Group 1" или как называется)
3. Add -> Trim Paths (через кнопку Add справа от Contents)
4. Теперь Trim Paths внутри группы — всё правильно
```

---

## БЛОК 14: ТОЛПА — все слои одинаковые

### Проблема: Скопировал слой 20 раз, все двигаются одинаково

```
ПРИЧИНА: При копировании слоёв они получают разные index,
НО если expression не использует index — все одинаковые.

БЫСТРЫЙ ФИКС — добавь index в seed:
// Было (одинаково для всех):
wiggle(2, 50);

// Стало (каждый свой паттерн):
seedRandom(index * 37, true);
wiggle(2, 50);

ДЛЯ POSITION:
// Было:
w = wiggle(1, 80);
[value[0] + w[0], value[1] + w[1]];

// Стало (разные траектории):
seedRandom(index * 41, true);
freqX = random(0.3, 1.2);
freqY = random(0.2, 0.9);
phX   = random(0, Math.PI * 2);
phY   = random(0, Math.PI * 2);
ampX  = random(30, 100);
ampY  = random(20, 70);
ox = Math.sin(time * freqX * Math.PI * 2 + phX) * ampX;
oy = Math.sin(time * freqY * Math.PI * 2 + phY) * ampY;
[value[0] + ox, value[1] + oy];
```

### Проблема: index одинаковый у всех слоёв в Pre-comp

```
ПРИЧИНА: Если слои находятся в Pre-comp — их index внутри Pre-comp
свой (1, 2, 3...). Но если Pre-comp сам скопирован несколько раз —
внутри каждой копии индексы одинаковые.

РЕШЕНИЕ: Использовать comp-level index через parent comp:
// Этот expression внутри Pre-comp читает index Pre-comp слоя
// в родительском компе:
thisComp.layer(thisLayer.name).index;
// Это нестандартно и часто не работает.

ПРАВИЛЬНОЕ РЕШЕНИЕ:
Не копировать Pre-comp, а создавать разные Pre-comp-ы,
или работать без Pre-comp для элементов с уникальной анимацией.

АЛЬТЕРНАТИВА: Slider Control с "ID"
1. На каждый слой в Pre-comp добавь Slider Control "Layer ID"
2. Вручную поставь значения: 1, 2, 3, 4...
3. В expression читай этот Slider как "ID":
   myID = thisLayer.effect("Layer ID")("Slider");
   seedRandom(myID * 41, true);
   wiggle(2, 50);
```

---

## БЛОК 15: РЕНДЕР — в превью работает, в рендере нет

### Проблема: Expressions работают в превью, но неправильно в рендере

```
ПРИЧИНА 1: Рендер использует другой frame rate
РЕШЕНИЕ:
- Composition Settings -> Frame Rate = должен совпадать с Output Module
- Если превью на 24fps, рендер на 25fps — time ведёт себя по-другому

ПРИЧИНА 2: Кэш превью устарел
РЕШЕНИЕ:
- Edit -> Purge -> All Memory and Disk Cache
- Рендери заново

ПРИЧИНА 3: Expression зависит от случайного состояния
// seedRandom(false) = разный каждый кадр при каждом воспроизведении
// Между превью и рендером = разные результаты
РЕШЕНИЕ: seedRandom(seed, true) — фиксированный seed

ПРИЧИНА 4: Рендер идёт через Media Encoder, а не через AE
РЕШЕНИЕ: Рендери напрямую из AE: Composition -> Add to Render Queue
Media Encoder иногда ведёт себя иначе с expressions.
```

### Проблема: Expression error только в рендере

```
ДИАГНОСТИКА:
1. File -> Save (сохрани проект)
2. Composition -> Add to Render Queue
3. Render
4. Если ошибка — AE покажет в каком слое и какое expression
5. Найди слой, исправь

ТИПИЧНАЯ ПРИЧИНА:
- В рендере AE более строгий к типам данных
- Например: position.valueAtTime() в превью молча возвращает [0,0]
  при недоступном времени, в рендере — кидает ошибку
РЕШЕНИЕ:
try {
  pos = otherLayer.transform.position.valueAtTime(time - 0.1);
} catch(e) {
  pos = [thisComp.width/2, thisComp.height/2];  // fallback
}
pos;
```

---

## БЛОК 16: ДИАГНОСТИКА — как найти проблему самому

### Метод 1: Текстовый монитор

```
САМЫЙ ПОЛЕЗНЫЙ ИНСТРУМЕНТ — выводи значения как текст:

1. Layer -> New -> Text
2. Alt+Click на Source Text
3. Введи:
   // Показывает всё что нужно:
   audioLayer = thisComp.layer("Audio Amplitude");
   amp = audioLayer.effect("Both Channels")("Slider");
   
   "amp: " + Math.round(amp * 10) / 10
   + "\ntime: " + Math.round(time * 100) / 100
   + "\nframe: " + Math.floor(time * thisComp.frameRate);
4. Нажми Space — смотри значения в реальном времени
5. После отладки — скрой или удали слой
```

### Метод 2: Изолируй expression по частям

```
КОГДА expression сложный и что-то не так:

СТРАТЕГИЯ:
1. Упрости до минимума:
   // Было (сложное):
   audioLayer = thisComp.layer("Audio Amplitude");
   amp = audioLayer.effect("Both Channels")("Slider");
   s = ease(amp, 0, 20, 100, 200);
   boost = wiggle(3, s * 0.1)[0];
   [s + boost, s + boost];
   
   // Шаг 1: проверь только амплитуду:
   audioLayer = thisComp.layer("Audio Amplitude");
   amp = audioLayer.effect("Both Channels")("Slider");
   [amp * 5, amp * 5];  // работает? -> амплитуда есть
   
   // Шаг 2: добавь ease:
   s = ease(amp, 0, 20, 100, 200);
   [s, s];  // работает? -> ease правильный
   
   // Шаг 3: добавь wiggle:
   // и т.д.
   
2. Находишь шаг где сломалось -> чинишь только его
```

### Метод 3: Проверка через Effect Controls

```
СПОСОБ БЫСТРО УВИДЕТЬ ЗНАЧЕНИЕ SLIDER:
1. Выдели слой с Slider Control
2. Window -> Effect Controls (или Ctrl+5)
3. Нажми Space
4. Slider должен двигаться в такт музыке
5. Если стоит — expression на Slider не работает
6. Кликни на значение Slider — увидишь expression под ним
```

### Метод 4: Expression error log

```
AE ЗАПИСЫВАЕТ ОШИБКИ:
1. Edit -> Preferences -> General
2. Найди "Write expression errors to console" (если есть)
3. Или смотри в: Window -> Info
4. Ошибки expressions появляются в Info с номером кадра

ТАКЖЕ:
Если expression выдаёт ошибку — в таймлайне
под слоем появляется красная строка.
Нажми на неё — откроется Expression Editor с ошибкой.
Ошибка подсвечивается и описывается внизу редактора.
```

### Метод 5: Бинарный поиск в сложном expression

```
КОГДА expression длинный и непонятно где ошибка:

// Закомментируй половину expression и проверь:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 200);
// Пока закомментировано — проверяем что до здесь всё ок:
[s, s];

// Если работает — раскомментируй вторую половину:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 200);
w = wiggle(3, s * 0.1)[0];  // раскомментировали
[s + w, s + w];  // и это

// Метод деления пополам — находишь проблему за 3-4 итерации
// даже в expression на 50 строк
```

### Чеклист самодиагностики

```
Если что-то не работает — пройди по списку:

□ Иконка секундомера ЖЁЛТАЯ? (expression активен)
□ Нет красного текста под слоем? (нет ошибки синтаксиса)
□ Слой [Audio Amplitude] существует в компе?
□ Имя слоя в expression ТОЧНО совпадает с именем в таймлайне?
□ Имя эффекта ТОЧНО совпадает (регистр, пробелы)?
□ Для Position: возвращаешь [x, y], а не одно число?
□ Для Scale: возвращаешь [x, y], а не одно число?
□ Для 3D слоёв: возвращаешь [x, y, z]?
□ Для Source Text: возвращаешь строку, не число?
□ tMax в ease() соответствует реальному максимуму амплитуды?
□ Нет прямых ссылок на [Audio Amplitude] с 10+ слоёв?
   (если да -> переходи на Null + Slider Control)
□ AE кэш не устарел? (Edit -> Purge -> All)
```

---

## 🔧 БЫСТРЫЙ СПРАВОЧНИК

```
// ── МАППИНГ ──────────────────────────────────────────────────────
linear(t, tMin, tMax, val1, val2)      — линейный маппинг
ease(t, tMin, tMax, val1, val2)        — с плавными краями (оба)
easeIn(t, tMin, tMax, val1, val2)      — плавный вход, резкий выход
easeOut(t, tMin, tMax, val1, val2)     — резкий вход, плавный выход
clamp(v, min, max)                     — ограничитель диапазона

// ── ШУМ И РАНДОМ ─────────────────────────────────────────────────
wiggle(freq, amp, octaves, ampMult, t) — шум Перлина
random(min, max)                       — случайное число
seedRandom(seed, timeless)             — инициализация рандома
                                         timeless=true — фиксирует seed
// ── МАТЕМАТИКА ───────────────────────────────────────────────────
Math.sin(t)                            — синус (-1..1)
Math.cos(t)                            — косинус (-1..1)
Math.PI                                — 3.14159...
Math.abs(v)                            — модуль числа
Math.floor(v)                          — округление вниз
Math.ceil(v)                           — округление вверх
Math.round(v)                          — округление
Math.sqrt(v)                           — квадратный корень
Math.exp(v)                            — e в степени v (затухание!)
Math.pow(base, exp)                    — степень
Math.min(a, b)                         — минимум двух чисел
Math.max(a, b)                         — максимум двух чисел

// ── ВРЕМЯ И СЛОЙ ─────────────────────────────────────────────────
time                                   — текущее время в секундах
thisComp.frameDuration                 — длительность одного кадра
value                                  — текущее кейфреймовое значение
valueAtTime(t)                         — значение свойства в момент t
index                                  — номер слоя (уникален, с 1)
thisComp.width / thisComp.height       — размеры компа

// ── ГЕОМЕТРИЯ ────────────────────────────────────────────────────
length(v1, v2)                         — расстояние между двумя точками
normalize(v)                           — вектор длиной 1
add(v1, v2)                            — сложение векторов
sub(v1, v2)                            — вычитание векторов
mul(v, scalar)                         — умножение вектора на скаляр
dot(v1, v2)                            — скалярное произведение
cross(v1, v2)                          — векторное произведение

// ── КООРДИНАТЫ ───────────────────────────────────────────────────
toComp(point)                          — из локальных в comp-координаты
fromComp(point)                        — из comp в локальные
toWorld(point)                         — в мировые координаты
fromWorld(point)                       — из мировых в локальные
```

### Формулы которые надо знать наизусть

```javascript
// Нормализация 0..1:
t = clamp((x - min) / (max - min), 0, 1);

// Smoothstep (ease без аргументов диапазона):
st = t * t * (3 - 2 * t);

// Lerp (линейная интерполяция):
result = a + (b - a) * t;

// Синус туда-сюда:
Math.sin(time * freq * Math.PI * 2) * amp;

// Затухание (decay):
initial * Math.exp(-rate * time);

// Дискретный шаг (N раз в секунду):
Math.floor(time * N);

// Треугольная волна:
Math.abs(2 * ((time * freq) - Math.floor(time * freq + 0.5)));

// Пила:
(time * freq) % 1;

// Прямоугольная волна (0 или 1):
Math.floor((time * freq) % 2);
```

---

## БЛОК 17: SMOOTH MOTION И СИНУС — не то что ожидал

### Проблема: Синусоида слишком быстрая или медленная

```
ОБЪЯСНЕНИЕ ПАРАМЕТРА freq:
Math.sin(time * freq * Math.PI * 2) * amp

freq = 1.0  ->  1 полный цикл в секунду (туда и обратно за 1 сек)
freq = 0.5  ->  1 цикл за 2 секунды (медленно)
freq = 2.0  ->  2 цикла в секунду (быстро)
freq = 0.1  ->  1 цикл за 10 секунд (очень медленно, дрейф)

СВЯЗЬ С BPM:
BPM 120 = 2 удара в секунду = freq 2.0 (пульс каждый удар)
BPM 120 = каждый второй удар = freq 1.0
BPM 120 = каждый такт (4/4)  = freq 0.5

ФОРМУЛА:
freq = BPM / 60 / делитель
// делитель 1 = каждый удар
// делитель 2 = каждые два удара
// делитель 4 = каждый такт

ПРИМЕР:
bpm  = 128;
freq = bpm / 60 / 4;  // пульс раз в такт
Math.sin(time * freq * Math.PI * 2) * 50;
```

### Проблема: Синусоида не начинается с нуля (сдвинута)

```
ПРИЧИНА: Когда комп не начинается с 0:00, time != 0 в начале.
Или хочешь сдвинуть фазу осознанно.

РЕШЕНИЕ — фазовый сдвиг:
phase = 0;             // 0     = начинает с 0, идёт вверх
phase = Math.PI / 2;   // 90°   = начинает с максимума
phase = Math.PI;       // 180°  = начинает с 0, идёт вниз
phase = Math.PI * 1.5; // 270°  = начинает с минимума

freq = 1.0;
amp_ = 50;
Math.sin(time * freq * Math.PI * 2 + phase) * amp_;

ДЛЯ КАЖДОГО СЛОЯ СВОЯ ФАЗА (толпа):
seedRandom(index * 23, true);
phase = random(0, Math.PI * 2);  // случайная фаза 0..360°
Math.sin(time * freq * Math.PI * 2 + phase) * amp_;
```

### Проблема: Затухающее колебание (decay oscillation) начинается не вовремя

```
СТРУКТУРА ФОРМУЛЫ:
startTime = 1.5;   // когда начинается колебание (секунды от начала компа)
freq      = 5.0;
decay     = 3.0;
initAmp   = 80;

t = time - startTime;  // время ОТНОСИТЕЛЬНО момента старта
if (t < 0) {
  value;  // до startTime — стоим на месте
} else {
  // Затухающая синусоида:
  envelope = Math.exp(-decay * t);   // убывает от 1 до 0
  wave     = Math.sin(freq * Math.PI * 2 * t);
  value + envelope * initAmp * wave;
}

ЧАСТАЯ ОШИБКА — используют time вместо t:
// НЕПРАВИЛЬНО: Math.exp(-decay * time) — decay считается от начала компа
// ПРАВИЛЬНО:   Math.exp(-decay * t)    — decay считается от момента удара

ПОДБОР ПАРАМЕТРОВ:
decay = 1.0  -> долгое затухание (~3 секунды)
decay = 3.0  -> среднее (~1 секунда)
decay = 8.0  -> быстрое (~0.3 секунды, резкий отскок)

freq = 2.0  -> медленные колебания (видны все волны)
freq = 6.0  -> быстрые колебания (много мелких качков)
freq = 12.0 -> очень быстро (вибрация)
```

### Проблема: Step random (дискретные прыжки) дёргается слишком резко

```
ПРИЧИНА: Используешь версию без интерполяции между шагами.

БЕЗ ИНТЕРПОЛЯЦИИ (резкие прыжки):
interval = 0.5;
stepTime  = Math.floor(time / interval) * interval;
seedRandom(stepTime * 1000 + index, true);
random(-80, 80);  // прыгает мгновенно

С ЛИНЕЙНОЙ ИНТЕРПОЛЯЦИЕЙ (скользит):
interval = 0.5;
t        = time / interval;
tFloor   = Math.floor(t);
tFrac    = t - tFloor;          // 0..1 прогресс внутри шага

seedRandom(tFloor * 100 + index, true);
v1 = random(-80, 80);           // текущая точка
seedRandom((tFloor + 1) * 100 + index, true);
v2 = random(-80, 80);           // следующая точка
v1 + (v2 - v1) * tFrac;        // линейно скользим между ними

С EASE ИНТЕРПОЛЯЦИЕЙ (плавно тормозит):
interval = 0.5;
t        = time / interval;
tFloor   = Math.floor(t);
tFrac    = t - tFloor;
st       = tFrac * tFrac * (3 - 2 * tFrac);  // smoothstep

seedRandom(tFloor * 100 + index, true);
v1 = random(-80, 80);
seedRandom((tFloor + 1) * 100 + index, true);
v2 = random(-80, 80);
v1 + (v2 - v1) * st;  // ease скользим

ПОДБОР interval:
interval = 0.125  -> прыжок каждые 1/8 секунды (очень быстро)
interval = 0.25   -> каждые 1/4 секунды
interval = 0.5    -> каждые полсекунды
interval = 1.0    -> каждую секунду
interval = 60/BPM -> каждый удар (синхронно с треком!)
```

---

## БЛОК 18: INTERPOLATION И LERP — проблемы с переходами

### Проблема: Lerp между точками телепортируется вместо плавного движения

```
ПРИЧИНА: t выходит за пределы 0..1 или не нормализован.

ПРАВИЛО LERP:
t = 0   -> точка A
t = 0.5 -> середина
t = 1   -> точка B
t > 1   -> ВЫХОДИТ ЗА B (экстраполяция — может телепортировать!)

РЕШЕНИЕ — всегда clamp:
duration = 3.0;
t = clamp(time / duration, 0, 1);  // ОБЯЗАТЕЛЬНО clamp!
// Без clamp: при time > duration -> t > 1 -> слой улетает

// Проверка:
t = clamp(time / duration, 0, 1);  // 0..1 гарантировано
x = 100 + (900 - 100) * t;         // 100..900 гарантировано
[x, value[1]];
```

### Проблема: Движение по массиву точек (waypoints) — слой застревает

```
ПРИЧИНА: seg выходит за пределы массива.

ТИПИЧНАЯ ОШИБКА:
points = [[100,300], [500,100], [900,300]];
segDur = 1.5;
seg    = Math.floor(time / segDur);  // при time=5: seg=3, а points[3] = undefined!

РЕШЕНИЕ — добавь min():
points = [[100,300], [500,100], [900,300]];
segDur = 1.5;
totalTime = segDur * (points.length - 1);
t    = clamp(time, 0, totalTime);   // не выходим за конец маршрута
seg  = Math.min(
         Math.floor(t / segDur),
         points.length - 2          // максимум = предпоследняя точка
       );
tSeg = (t - seg * segDur) / segDur;
st   = tSeg * tSeg * (3 - 2 * tSeg);

A = points[seg];
B = points[seg + 1];
[A[0] + (B[0] - A[0]) * st,
 A[1] + (B[1] - A[1]) * st];
```

---

## БЛОК 19: СВЯЗЬ МЕЖДУ СЛОЯМИ — не находит слой

### Проблема: thisComp.layer("ИМЯ") — cannot find layer

```
ПОЛНЫЙ ЧЕКЛИСТ:

1. РЕГИСТР:
   thisComp.layer("beat_master")  // НЕПРАВИЛЬНО
   thisComp.layer("BEAT_MASTER")  // ПРАВИЛЬНО
   // AE чувствителен к регистру!

2. ПРОБЕЛЫ В КОНЦЕ:
   // Иногда при переименовании добавляется пробел:
   "BEAT_MASTER "  // пробел в конце — не видно, но слой не найдёт
   // Решение: двойной клик на имя слоя -> выдели всё -> перепечатай заново

3. СЛОЙ В ДРУГОМ КОМПЕ:
   // thisComp.layer() ищет только в ТЕКУЩЕМ компе
   // Если слой в Pre-comp — из родительского компа его не видно
   // Решение: положи BEAT_MASTER в тот же комп где используешь его

4. СЛОЙ ВЫКЛЮЧЕН (shy):
   // Shy слои (иконка человечка) скрыты из таймлайна визуально,
   // но thisComp.layer() их НАХОДИТ — это не проблема.
   // Но если слой Solo — другие могут вести себя иначе.

5. СЛОЙ ЗА ПРЕДЕЛАМИ WORK AREA:
   // Если [Audio Amplitude] короче чем комп — в конце амплитуда = 0
   // Решение: убедись что слой тянется на весь комп

ДИАГНОСТИКА:
// Добавь на Source Text:
thisComp.numLayers + " layers in comp";
// Показывает сколько слоёв AE видит. Посчитай сам — совпадает?
```

### Проблема: Pick Whip создал ссылку, но она не работает после переноса в другой комп

```
ПРИЧИНА: Pick Whip создаёт ссылку по имени слоя.
При копировании comp в другой проект — имена сохраняются,
но если слой отсутствует — ошибка.

РЕШЕНИЕ:
При копировании comp всегда копируй ВСЕ связанные слои вместе.
Ctrl+A (выдели все в исходном компе) -> Ctrl+C -> вставляй в новый комп.
```

---

## БЛОК 20: SHAPE LAYERS — продвинутые проблемы

### Проблема: Repeater Copies дробное число — шейп мигает

```
ПРИЧИНА: Copies должно быть целым числом. Дробное = нестабильное поведение.

РЕШЕНИЕ — всегда Math.round():
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
Math.round(ease(amp, 0, 20, 1, 12));
//          ^^^^^^^^^^^ обязательно!

ТО ЖЕ ДЛЯ:
- Polystar -> Points: Math.round(...)
- Mosaic -> Horizontal/Vertical Blocks: Math.round(...)
- Echo -> Number of Echoes: Math.round(...)
- Любое свойство ожидающее целое число
```

### Проблема: Trim Paths End = 100, но линия не рисуется полностью

```
ПРИЧИНА 1: Start > 0 — обрезает начало.
ПРОВЕРЬ: Contents -> [Group] -> Trim Paths -> Start = 0?

ПРИЧИНА 2: Trim Paths снаружи группы с путём.
СТРУКТУРА ДОЛЖНА БЫТЬ:
Contents
  └── Group 1
        ├── Path 1      <- сам путь
        ├── Stroke 1    <- обводка
        └── Trim Paths  <- ЗДЕСЬ, внутри группы

СТРУКТУРА НЕ РАБОТАЕТ:
Contents
  ├── Group 1
  │     ├── Path 1
  │     └── Stroke 1
  └── Trim Paths  <- ЗДЕСЬ НЕ РАБОТАЕТ (снаружи группы)

ПРИЧИНА 3: Trim Based On = неправильное значение.
Contents -> Trim Paths -> Trim Based On:
= Simultaneously  -> все пути обрезаются вместе (обычно это нужно)
= Individually    -> каждый путь независимо

ПРИЧИНА 4: Stroke нет или Stroke Width = 0.
Trim Paths работает, но без видимой обводки — ничего не видно.
Добавь: Contents -> [Group] -> Add -> Stroke.
```

### Проблема: Dash Offset не двигает пунктир

```
ПРИЧИНА: Нет настроенных Dashes.

КАК ПРАВИЛЬНО:
1. Contents -> Shape -> Stroke -> Dashes
2. Нажми + (плюс) рядом с Dashes — добавляется "Dash"
3. Нажми + ещё раз — добавляется "Gap"
4. Теперь появился "Offset" — вешай expression на него
5. Dash = длина черточки, Gap = длина пробела

// Offset expression:
time * 100;  // движется вправо
-(time * 100);  // движется влево

// Под бит:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
baseSpeed = 80;
beatBoost  = ease(amp, 0, 20, 0, 300);
(baseSpeed + beatBoost) * time;
```

---

## БЛОК 21: TEXT EXPRESSIONS — продвинутые проблемы

### Проблема: Глитч-текст показывает одинаковые символы на всех кадрах

```
ПРИЧИНА: seed не меняется от кадра к кадру.
seedRandom(index * 41, true) — true = ФИКСИРОВАННЫЙ seed.
Для глитча нужно true чтобы seed был фиксирован ПО ПОЗИЦИИ СИМВОЛА,
но менялся ОТ КАДРА К КАДРУ.

ПРАВИЛЬНАЯ СХЕМА ДЛЯ ГЛИТЧА:
chars  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
fps    = thisComp.frameRate;
frame  = Math.floor(time * fps);   // номер кадра — меняется каждый кадр
len    = 8;
result = "";

for (i = 0; i < len; i++) {
  // seed = кадр * длина + позиция символа
  // -> каждый кадр новый seed -> разные символы каждый кадр
  // -> каждый символ свой seed -> не все одинаковые
  seedRandom(frame * len + i, true);
  idx = Math.floor(random(0, chars.length));
  result += chars[idx];
}
result;

МЕДЛЕННЫЙ ГЛИТЧ (меняется не каждый кадр, а каждые N кадров):
fps       = thisComp.frameRate;
glitchFPS = 8;   // 8 раз в секунду, а не 24/30
frame     = Math.floor(time * glitchFPS);  // дискретизируем время
// Дальше то же самое с frame
```

### Проблема: Счётчик скачет нелинейно или идёт назад

```
ПРИЧИНА: smoothstep или ease дают нелинейное нарастание — визуально
кажется что счётчик то быстрее то медленнее.

ДЛЯ РАВНОМЕРНОГО СЧЁТЧИКА — используй линейный t:
startVal = 0;
endVal   = 1000;
duration = 3.0;
t = clamp(time / duration, 0, 1);  // линейный, без ease
Math.round(startVal + (endVal - startVal) * t);

ДЛЯ СЧЁТЧИКА С РАЗГОНОМ И ТОРМОЖЕНИЕМ — smoothstep:
t  = clamp(time / duration, 0, 1);
st = t * t * (3 - 2 * t);  // нелинейно — выглядит эффектно
Math.round(startVal + (endVal - startVal) * st);

ДЛЯ СЧЁТЧИКА ТОЛЬКО С ТОРМОЖЕНИЕМ — easeIn-like:
t  = clamp(time / duration, 0, 1);
st = t * t;  // квадратичный разгон -> тормозит плавно в конце
Math.round(startVal + (endVal - startVal) * st);
```

---

## БЛОК 22: ПРОИЗВОДИТЕЛЬНОСТЬ — продвинутые случаи

### Проблема: Expression с циклом for тормозит

```
ПРИЧИНА: Длинный цикл for пересчитывается КАЖДЫЙ КАДР для КАЖДОГО СЛОЯ.

// МЕДЛЕННО — O(n) каждый кадр:
result = "";
for (i = 0; i < 100; i++) {
  seedRandom(i * 13, true);
  result += random(0, 9);
}
result;

ОПТИМИЗАЦИЯ 1: Сократи количество итераций
// Нужно ли 100 символов? Может хватит 12?
for (i = 0; i < 12; i++) { ... }

ОПТИМИЗАЦИЯ 2: Вынеси стабильные вычисления наружу
// Плохо — пересчитывается в каждой итерации:
for (i = 0; i < len; i++) {
  fps   = thisComp.frameRate;        // считается len раз!
  frame = Math.floor(time * fps);    // считается len раз!
  seedRandom(frame * len + i, true);
  // ...
}

// Хорошо — один раз до цикла:
fps   = thisComp.frameRate;
frame = Math.floor(time * fps);
for (i = 0; i < len; i++) {
  seedRandom(frame * len + i, true);  // frame уже готов
  // ...
}

ОПТИМИЗАЦИЯ 3: Перенеси тяжёлые вычисления на Null
// Если 20 слоёв используют одинаковый цикл — положи на Null,
// остальные читают результат как Slider.
```

### Проблема: Expression с Math.exp / Math.sqrt тормозит

```
ПРИЧИНА: Тригонометрия и экспоненты — тяжёлые операции.
На 1-2 слоях незаметно. На 50+ слоях — может лагать.

ОПТИМИЗАЦИЯ: Кэшируй на Null
// Вместо Math.exp(-decay * time) на каждом из 50 слоёв:
// Поставь на Null -> Slider "Decay Envelope":
Math.exp(-2.0 * time);
// Все 50 слоёв читают готовое число:
null_.effect("Decay Envelope")("Slider");
```

### Таблица производительности операций (от быстрой к медленной)

```
БЫСТРО:
+ - * /                    — базовая арифметика
clamp, Math.min, Math.max  — сравнения
value, index, time         — встроенные переменные
Slider Control чтение      — простое чтение числа

СРЕДНЕ:
Math.sin, Math.cos         — тригонометрия
Math.floor, Math.round     — округления
random(), seedRandom()     — генерация рандома
wiggle()                   — шум Перлина

МЕДЛЕННО:
Math.sqrt                  — квадратный корень
Math.exp                   — экспонента
Math.log, Math.atan2       — логарифм, арктангенс
length(), normalize()      — векторные операции

ОЧЕНЬ МЕДЛЕННО:
valueAtTime()              — перемотка анимации
sourceRectAtTime()         — геометрия слоя
Циклы for с 50+ итерациями — множественные вычисления

ПРАВИЛО:
Всё из "МЕДЛЕННО" и "ОЧЕНЬ МЕДЛЕННО" на Null -> Slider.
Рабочие слои читают только числа.
```

---

## БЛОК 23: ТИПИЧНЫЕ ПАТТЕРНЫ ОШИБОК И ИХ РЕШЕНИЯ

### Паттерн: "Написал expression — ничего не изменилось"

```
ЧЕКЛИСТ (пройди по порядку, остановись когда найдёшь):

□ Шаг 1: Иконка секундомера жёлтая?
  НЕТ -> Alt+Click на неё и введи expression заново

□ Шаг 2: Есть красный текст под слоем?
  ДА -> Синтаксическая ошибка. Кликни на красный текст, читай ошибку.

□ Шаг 3: Expression возвращает правильный тип?
  Scale/Position -> [x, y] (массив)
  Opacity/Rotation -> одно число
  Source Text -> строка ("")
  
□ Шаг 4: Слой [Audio Amplitude] существует и назван правильно?
  Animation -> Keyframe Assistant -> Convert Audio to Keyframes

□ Шаг 5: Нажми U на слое — видны ли все expression свойства?
  ДА -> expression есть, но может не реагировать из-за tMax
  
□ Шаг 6: Выведи амплитуду как текст (см. Блок 16) — есть ли значения?
  НЕТ (всегда 0) -> проблема в аудио (Блок 4)
  ДА (цифры есть) -> проблема в tMax или маппинге (Блок 6)
```

### Паттерн: "Раньше работало, теперь нет"

```
ЧТО ОБЫЧНО МЕНЯЕТСЯ:

1. Переименовал слой -> все ссылки на него сломались
   Решение: верни старое имя или обнови все expressions

2. Переместил слой в Pre-comp -> expression не видит его в текущем компе
   Решение: вынеси нужный слой из Pre-comp или обнови путь

3. Добавил/удалил эффект на [Audio Amplitude] -> изменился порядок эффектов
   Если используешь .effect(1) по индексу — теперь другой эффект
   Решение: всегда используй имена: .effect("Both Channels")

4. Изменил размер компа -> хардкодные координаты неправильные
   Решение: используй value[], thisComp.width, thisComp.height

5. AE обновился -> изменился синтаксис или поведение функции
   Решение: проверь release notes AE
```

### Паттерн: "Expression работает, но выглядит не так"

```
ЧАСТЫЕ ПРИЧИНЫ:

1. Неправильный диапазон tMin/tMax
   -> Откалибруй через текстовый монитор амплитуды (Блок 16)

2. Неправильный выбор ease/easeIn/easeOut/linear
   -> Таблица в Блоке 6

3. Слишком высокая freq в синусе -> движение слишком быстрое
   -> Уменьши freq вдвое

4. Амплитуда влияет на неправильную ось
   -> Проверь что ox/oy перепутаны

5. Position смещается от неправильной точки (не от центра)
   -> Проверь Anchor Point (Блок 7)

6. Scale трансформируется не от нужной точки
   -> Anchor Point в нужный угол (Блок 7 и ⚓ ANCHOR POINT раздел)
```

---

## 📊 ДИАПАЗОНЫ АМПЛИТУДЫ — ОРИЕНТИРЫ

| Сигнал | Обычный диапазон amp |
|--------|---------------------|
| Тишина / пауза | 0 – 2 |
| Бэкграунд / атмосфера | 2 – 8 |
| Средний уровень | 8 – 18 |
| Удар / bass hit | 15 – 30 |
| Клипинг / максимум | 30+ |

> Калибруй `tMax` в ease/linear под конкретный трек — каждый трек разный!

---

## 📋 МАСТЕР-ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ ПРОЕКТА

```
EXPRESSIONS:
□ Все прямые ссылки на [Audio Amplitude] заменены на Null + Slider?
□ Все слои с разными id используют seedRandom(index * PRIME, true)?
□ Все массивы правильной размерности? ([x,y] для 2D, [x,y,z] для 3D)
□ Все Source Text возвращают строки, а не числа?
□ Нет хардкода координат (использую value[], thisComp.width)?
□ clamp() стоит там где нужно ограничить диапазон?
□ Math.round() стоит на всех свойствах ожидающих целые числа?

АУДИО:
□ [Audio Amplitude] создан и тянется на весь комп?
□ tMax откалиброван под реальный максимум этого трека?
□ tMin поднят если в тишине шум (> 0)?

ПРОИЗВОДИТЕЛЬНОСТЬ:
□ Нет valueAtTime() в цикле?
□ Тяжёлые вычисления (Math.exp, sqrt) на Null, не на каждом слое?
□ Кэш очищен перед финальным рендером?

СТРУКТУРА:
□ Null "BEAT_MASTER" с Beat Raw, Beat Smooth, Beat Sharp?
□ Все технические слои заблокированы (Lock) чтобы не сдвинуть?
□ Все expressions задокументированы комментариями (// что делает)?
□ Pre-comp не ломает ссылки на слои?
```

---

## 🔧 БЫСТРЫЙ СПРАВОЧНИК — ПОЛНЫЙ

```
// ── МАППИНГ ──────────────────────────────────────────────────────
linear(t, tMin, tMax, val1, val2)      — линейный маппинг
ease(t, tMin, tMax, val1, val2)        — с плавными краями (оба)
easeIn(t, tMin, tMax, val1, val2)      — плавный вход, резкий выход
easeOut(t, tMin, tMax, val1, val2)     — резкий вход, плавный выход
clamp(v, min, max)                     — ограничитель диапазона

// ── ШУМ И РАНДОМ ─────────────────────────────────────────────────
wiggle(freq, amp, octaves, ampMult, t) — шум Перлина
random(min, max)                       — случайное число
seedRandom(seed, timeless)             — инициализация рандома
                                         timeless=true — фиксирует seed

// ── МАТЕМАТИКА ───────────────────────────────────────────────────
Math.sin(t)                            — синус (-1..1)
Math.cos(t)                            — косинус (-1..1)
Math.PI                                — 3.14159...
Math.abs(v)                            — модуль числа
Math.floor(v)                          — округление вниз
Math.ceil(v)                           — округление вверх
Math.round(v)                          — округление
Math.sqrt(v)                           — квадратный корень
Math.exp(v)                            — e в степени v (затухание!)
Math.pow(base, exp)                    — степень
Math.min(a, b)                         — минимум двух чисел
Math.max(a, b)                         — максимум двух чисел

// ── ВРЕМЯ И СЛОЙ ─────────────────────────────────────────────────
time                                   — текущее время в секундах
thisComp.frameDuration                 — длительность одного кадра
thisComp.frameRate                     — кадров в секунду
thisComp.numLayers                     — количество слоёв в компе
thisComp.width / thisComp.height       — размеры компа
value                                  — текущее кейфреймовое значение
valueAtTime(t)                         — значение свойства в момент t
index                                  — номер слоя (уникален, с 1)
inPoint / outPoint                     — начало/конец слоя в секундах

// ── ГЕОМЕТРИЯ ────────────────────────────────────────────────────
length(v1, v2)                         — расстояние между двумя точками
normalize(v)                           — вектор длиной 1
add(v1, v2)                            — сложение векторов
sub(v1, v2)                            — вычитание векторов
mul(v, scalar)                         — умножение вектора на скаляр
dot(v1, v2)                            — скалярное произведение
cross(v1, v2)                          — векторное произведение

// ── КООРДИНАТЫ ───────────────────────────────────────────────────
toComp(point)                          — из локальных в comp-координаты
fromComp(point)                        — из comp в локальные
toWorld(point)                         — в мировые координаты
fromWorld(point)                       — из мировых в локальные

// ── ТЕКСТ И СЛОЙ ─────────────────────────────────────────────────
sourceRectAtTime(t)                    — геометрия слоя (width, height, top, left)
thisLayer.name                         — имя текущего слоя
thisComp.layer("name")                 — найти слой по имени
thisComp.layer(n)                      — найти слой по номеру
thisLayer.effect("name")("Slider")     — читать Slider Control
thisComp.marker.numKeys                — количество маркеров в компе
thisComp.marker.key(n).time            — время n-го маркера
```

### Формулы которые надо знать наизусть

```javascript
// Нормализация 0..1:
t = clamp((x - min) / (max - min), 0, 1);

// Smoothstep (плавный 0..1):
st = t * t * (3 - 2 * t);

// Lerp (линейная интерполяция между a и b):
result = a + (b - a) * t;

// Синус туда-сюда:
Math.sin(time * freq * Math.PI * 2) * amp;

// Синус с фазой (сдвиг старта):
Math.sin(time * freq * Math.PI * 2 + phase) * amp;

// Затухание (decay, убывает от initial до 0):
initial * Math.exp(-rate * time);

// Нарастание (растёт от 0 до 1):
1 - Math.exp(-rate * time);

// Дискретный шаг (N раз в секунду):
Math.floor(time * N);

// Треугольная волна (-1..1):
Math.abs(2 * ((time * freq) - Math.floor(time * freq + 0.5))) * 2 - 1;

// Пила (0..1):
(time * freq) % 1;

// Прямоугольная волна (0 или 1):
Math.floor((time * freq) % 2);

// Частота из BPM:
bpm / 60;           // ударов в секунду
bpm / 60 / 4;       // тактов в секунду (4/4)

// Случайная фаза для каждого слоя:
seedRandom(index * 31, true);
phase = random(0, Math.PI * 2);

// Стагер задержка по index:
delay = (index - 1) * 0.08;

// Позиция в сетке:
col = (index - 1) % cols;
row = Math.floor((index - 1) / cols);
```

---

*7000 строк. 200 кб. Анимируй всё. Бойся ничего.*
*Amplitude flows — ease catches it — objects dance.*
