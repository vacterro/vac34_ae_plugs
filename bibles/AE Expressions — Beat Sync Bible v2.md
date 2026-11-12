# 🎛️ AE Expressions — Beat Sync Bible v2

> Переписанная и расширенная версия. Пояснения, ручки, варианты и производственная логика.

## 📋 ОГЛАВЛЕНИЕ
> Кликабельное оглавление в стиле Obsidian: `[[#...]]` как в v1, без HTML-акробатики.

- [[#🔊 АУДИО — ОСНОВА ВСЕГО]]
  - [[#Ссылка на оба канала]]
  - [[#Левый и правый канал отдельно]]
  - [[#Ручное среднее]]
- [[#🎚️ АМПЛИТУДА — БАЗОВЫЕ ШАБЛОНЫ]]
  - [[#Сырой сигнал]]
  - [[#Усиление]]
  - [[#Маппинг через linear()]]
  - [[#Маппинг через ease()]]
  - [[#Clamp после усиления]]
- [[#📐 SCALE — МАСШТАБ]]
  - [[#Равномерный scale]]
  - [[#Squash & stretch]]
  - [[#Scale от базы + буст]]
  - [[#Появление из нуля]]
- [[#🔄 ROTATION — ВРАЩЕНИЕ]]
  - [[#Простой поворот]]
  - [[#Маятник]]
  - [[#Накопительный спин]]
  - [[#Отклик с wobble]]
- [[#📍 POSITION — ПОЗИЦИЯ]]
  - [[#Y-прыжок вверх]]
  - [[#X-сдвиг]]
  - [[#Orbit]]
  - [[#Shake]]
- [[#🔢 VALUE DIAL — КРУТИЛКА / ЧИСЛОВОЕ ЗНАЧЕНИЕ]]
  - [[#Обычная крутилка]]
  - [[#Инверсия]]
  - [[#Добавка к текущему value]]
- [[#🎨 OPACITY — ПРОЗРАЧНОСТЬ]]
  - [[#Dim под бит]]
  - [[#Вспышка]]
  - [[#Жёсткий threshold]]
  - [[#Soft threshold]]
- [[#📏 STROKE WIDTH — ТОЛЩИНА ОБВОДКИ]]
  - [[#Базовый stroke]]
  - [[#Stroke + clamp]]
- [[#🌈 COLOR — ЦВЕТ]]
  - [[#RGB реакция]]
  - [[#Hue shift]]
- [[#🎭 MULTI-PROPERTY — НЕСКОЛЬКО СВОЙСТВ СРАЗУ]]
  - [[#Beat master]]
  - [[#Scale из master]]
  - [[#Rotation из master]]
- [[#🏎️ EASING — СМЯГЧЕНИЯ]]
  - [[#linear()]]
  - [[#ease()]]
  - [[#easeIn / easeOut]]
  - [[#Manual curve]]
- [[#🔁 LOOP & REPEAT — ЦИКЛЫ]]
  - [[#loopOut cycle]]
  - [[#loopOut pingpong]]
  - [[#Синус-петля]]
- [[#⚡ WIGGLE + BEAT — ВИГЛ ПОД БИТ]]
  - [[#Базовый wiggle]]
  - [[#Wiggle от амплитуды]]
  - [[#Wiggle с seed]]
- [[#🎯 THRESHOLDS — ПОРОГОВЫЕ ЗНАЧЕНИЯ]]
  - [[#Binary trigger]]
  - [[#Multi-state]]
  - [[#Soft gate]]
- [[#📦 UTILS — ПОЛЕЗНЫЕ ФУНКЦИИ]]
  - [[#Normalize]]
  - [[#seedRandom + random]]
  - [[#Distance helper]]
- [[#🌊 SMOOTH MOTION — ПЛАВНОЕ ДВИЖЕНИЕ]]
  - [[#Синус]]
  - [[#Орбита]]
  - [[#Затухающее колебание]]
- [[#🎲 RANDOM MOTION — РАНДОМНОЕ ДВИЖЕНИЕ]]
  - [[#wiggle с редкой частотой]]
  - [[#Step random]]
  - [[#Staggered random]]
- [[#📡 INTERPOLATION — ИНТЕРПОЛЯЦИЯ МЕЖДУ ТОЧКАМИ]]
  - [[#lerp()]]
  - [[#smooth lerp]]
- [[#🔀 PROCEDURAL PATHS — ПРОЦЕДУРНЫЕ ТРАЕКТОРИИ]]
  - [[#Спираль]]
  - [[#Восьмёрка]]
- [[#🧲 FOLLOW & INERTIA — ИНЕРЦИЯ И СЛЕДОВАНИЕ]]
  - [[#Delay]]
  - [[#Follow leader]]
  - [[#Chain]]
- [[#🎛️ EXPRESSION CONTROLS — УПРАВЛЕНИЕ ЧЕРЕЗ UI]]
  - [[#Slider control]]
  - [[#Point control]]
  - [[#Checkbox]]
- [[#🔗 LINKING — СВЯЗЬ МЕЖДУ СЛОЯМИ]]
  - [[#Mirror position]]
  - [[#Inverse rotation]]
  - [[#Distance opacity]]
- [[#✍️ TEXT — РАБОТА С ТЕКСТОМ]]
  - [[#Source Text pulse]]
  - [[#Opacity for text]]
  - [[#Position for text]]
- [[#🖼️ SHAPE LAYERS — ШЕЙП-СЛОИ]]
  - [[#Trim Paths]]
  - [[#Shape height]]
- [[#🎬 TIME — РАБОТА СО ВРЕМЕНЕМ]]
  - [[#Time sine]]
  - [[#Time remap idea]]
- [[#📷 CAMERA — КАМЕРА]]
  - [[#Camera shake]]
  - [[#Rotation roll]]
- [[#💡 LIGHTS — СВЕТ]]
  - [[#Intensity]]
  - [[#Flicker]]
- [[#🌀 3D — ТРЁХМЕРНОЕ ПРОСТРАНСТВО]]
  - [[#3D scale]]
  - [[#Z push]]
- [[#🔢 COUNTERS & TIMERS — СЧЁТЧИКИ]]
  - [[#Timer]]
  - [[#Counter by beats]]
- [[#🎨 EFFECTS — КОНКРЕТНЫЕ ЭФФЕКТЫ]]
  - [[#Gaussian Blur]]
  - [[#Exposure]]
- [[#📐 MASKS & TRIM PATHS — МАСКИ И ОБРЕЗКА]]
  - [[#Trim End]]
- [[#🧮 MATH PATTERNS — МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ]]
  - [[#Clamp pattern]]
  - [[#Distance]]
- [[#🏗️ MASTER RIG v2 — PRODUCTION FULL RIG]]
  - [[#Master flow]]
  - [[#Use in scale]]
- [[#🎵 FREQUENCY BANDS — ЧАСТОТНЫЕ ДИАПАЗОНЫ]]
  - [[#Band idea]]
- [[#👥 CROWD RIG — ТОЛПЫ И МАССИВЫ]]
  - [[#Random crowd scale]]
  - [[#Crowd offset]]
- [[#⚓ ANCHOR POINT — ТОЧКА ТРАНСФОРМАЦИИ]]
  - [[#Anchor strategy]]
- [[#🎞️ COMP MARKERS — МАРКЕРЫ КОМПА]]
  - [[#Marker timing]]
- [[#🌊 ADVANCED WIGGLE — ПРОДВИНУТЫЙ ВИГЛ]]
  - [[#Octave wiggle]]
  - [[#Axis-specific]]
- [[#🎨 GRADIENT & COLOR ADVANCED — ЦВЕТ ПРОДВИНУТЫЙ]]
  - [[#Palette shift]]
- [[#🪆 PARENTING & NULL TRICKS — НУЛЛЫ И ПЭРЕНТИНГ]]
  - [[#Parent-based motion]]
- [[#💥 VFX SNIPPETS — ГОТОВЫЕ VFX СНИППЕТЫ]]
  - [[#Flash opacity]]
- [[#🔌 EXPRESSION TO EXPRESSION — ЦЕПОЧКИ]]
  - [[#Chain example]]
- [[#📊 DATA DRIVEN — ДАННЫЕ В АНИМАЦИЮ]]
  - [[#Concept]]
- [[#🏃 MOTION DESIGN PATTERNS — ПАТТЕРНЫ MOTION]]
  - [[#Pulse]]
- [[#🧰 ДИАГНОСТИКА И TROUBLESHOOTING]]
  - [[#Safe fallback]]
  - [[#Clamp everywhere]]
- [[#📋 МАСТЕР-ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ ПРОЕКТА]]
- [[#🗂️ WHAT WAS MISSING — ДОБАВЛЕННЫЕ СЕКЦИИ]]
  - [[#Attack / release]]
  - [[#Peak hold]]

## 🎛️ AE Expressions — Beat Sync Bible v2

Нормальная рабочая версия шпаргалки по expressions для After Effects: с пояснениями, ручками для креатива, запасными вариантами и блоками, которые обычно забывают, а потом героически чинят ночью.

**Креативные ручки:**

- Сначала ставь аудио-амплитуду через Convert Audio to Keyframes.
- Для всего, что прыгает от битов, держи отдельный control layer / null.
- Не пихай магию прямо в property, если можно вынести `Beat Raw`, `Beat Smooth`, `Beat Gate` и жить спокойнее.

---
## 🔊 АУДИО — ОСНОВА ВСЕГО

Сначала превращаешь звук в `Audio Amplitude`, потом уже кормишь им scale, position, opacity и прочие капризные свойства. Без этого шага выражения просто будут смотреть в пустоту, как люди в понедельник утром.

**Креативные ручки:**

- Имя слоя: чаще всего `Audio Amplitude`, но лучше вынести в helper/null и держать единый стандарт.
- Каналы: `Both`, `Left`, `Right`.
- Для стерео можно строить разные реакции по осям или по группам объектов.
### Ссылка на оба канала

Базовый способ взять усреднённый сигнал.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp;
```
### Левый и правый канал отдельно

Полезно для асимметричных реакций и стерео-движения.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider");
R = audioLayer.effect("Right Channel")("Slider");
[L, R, (L + R) / 2];
```
### Ручное среднее

Иногда звучит чуть ровнее, особенно если трек моно или центр тяжёлый.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
L = audioLayer.effect("Left Channel")("Slider").value;
R = audioLayer.effect("Right Channel")("Slider").value;
avg = (L + R) / 2;
avg;
```

---
## 🎚️ АМПЛИТУДА — БАЗОВЫЕ ШАБЛОНЫ

Это главная шина: берёшь амплитуду, нормализуешь, усиливаешь, обрезаешь, маппишь в удобный диапазон и только потом пихаешь в нужное property. Иначе будет не motion design, а припадок.

**Креативные ручки:**

- Множитель: усиливает реакцию без лишней алхимии.
- Clamp: отрезает пики и спасает от безумия.
- Linear / ease: маппинг в любой диапазон.
- Threshold: для включения/выключения.
### Сырой сигнал

Если нужен прямой отклик без обработки.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp;
```
### Усиление

Нужен более жирный удар? Умножай, как будто мир обязан тебе динамику.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp * 3;
```
### Маппинг через linear()

Самый предсказуемый перевод в новый диапазон.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
linear(amp, 0, 15, 100, 200);
```
### Маппинг через ease()

Чуть более органичный отклик.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 15, 100, 200);
```
### Clamp после усиления

Пики бывают слишком наглые. Режь их без жалости.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
clamp(amp * 5, 0, 100);
```

---
## 📐 SCALE — МАСШТАБ

Scale в AE это массив. Да, опять массив. Потому что один скейл человеческой душе показался бы слишком простым.

**Креативные ручки:**

- База: `baseScale`.
- Пик: `beatBoost`.
- Асимметрия по осям: `sx` и `sy`.
- Squash & stretch: отдельно сжимаешь и растягиваешь X/Y.
### Равномерный scale

Оба направления двигаются одинаково.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 150);
[s, s];
```
### Squash & stretch

Классика мультяшного импульса.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
sx = ease(amp, 0, 20, 100, 140);
sy = ease(amp, 0, 20, 100, 70);
[sx, sy];
```
### Scale от базы + буст

Если у слоя уже есть базовый размер, просто добавь реакцию сверху.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
base = 100;
boost = amp * 3;
s = base + boost;
[s, s];
```
### Появление из нуля

Удобно для intro и pop-in.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 25, 0, 100);
[s, s];
	```

---
## 🔄 ROTATION — ВРАЩЕНИЕ
	
Поворот под бит полезен, когда нужен визуальный удар, но без циркового коллапса. Тут важны пределы и направление.

**Креативные ручки:**

- Амплитуда поворота.
- Знак `-` для обратного вращения.
- Скорость для постоянного спина.
- Фаза и синус для качания.
### Простой поворот

Один удар - один угол.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 45);
```
### Маятник

Качание туда-сюда без кейфреймов.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
freq = ease(amp, 0, 20, 1, 6);
amount = ease(amp, 0, 20, 0, 25);
Math.sin(time * freq * Math.PI * 2) * amount;
```
### Накопительный спин

Если объект должен крутиться всё быстрее.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
speed = ease(amp, 0, 20, 0, 360);
speed * time;
```
### Отклик с wobble

Микро-раскачка после удара.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
base = ease(amp, 0, 20, 0, 30);
wobble = wiggle(8, amp * 1.5);
base + wobble;
```

---
## 📍 POSITION — ПОЗИЦИЯ

Сдвиг по позициям работает почти везде: текст, иконки, блики, частицы, камеры, всё это любит лишний импульс, пока ты не перестараешься.

**Креативные ручки:**

- X и Y можно двигать отдельно.
- Отрицательный Y = вверх, если ты не решил устроить себе психологическую проверку.
- Можно делать орбиты, шейки и задержки.
### Y-прыжок вверх

Самый простой beat punch.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
offset = ease(amp, 0, 20, 0, -80);
[value[0], value[1] + offset];
```
### X-сдвиг

Полезно для стерео-акцентов и сайд-панчей.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
offset = ease(amp, 0, 20, 0, 40);
[value[0] + offset, value[1]];
```
### Orbit

Круговое движение вокруг центра композиции.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
radius = ease(amp, 0, 20, 20, 120);
speed = 2;
cx = thisComp.width / 2;
cy = thisComp.height / 2;
[cx + Math.cos(time * speed * Math.PI * 2) * radius,
 cy + Math.sin(time * speed * Math.PI * 2) * radius];
```
### Shake

Мелкая тряска под бит.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amt = ease(amp, 0, 20, 0, 15);
freq = 20;
ox = Math.sin(time * freq * 6.28) * amt;
oy = Math.cos(time * freq * 6.28 * 0.7) * amt;
[value[0] + ox, value[1] + oy];
```

---
## 🔢 VALUE DIAL — КРУТИЛКА / ЧИСЛОВОЕ ЗНАЧЕНИЕ

Любой slider, angle или числовое поле можно превратить в реактивную ручку. Это удобно, когда нужно один раз настроить характер и дальше не ковыряться пальцем в макаронах.

**Креативные ручки:**

- Базовый диапазон.
- Инверсия.
- Добавка к существующему `value`.
- Отдельный контрол на null.
### Обычная крутилка

Линейный отклик 0..100.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```
### Инверсия

Тишина = максимум, удар = минимум.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 0);
```
### Добавка к текущему value

Когда базовое значение уже есть, а тебе нужна только реакция сверху.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
boost = ease(amp, 0, 20, 0, 50);
value + boost;
```

---
## 🎨 OPACITY — ПРОЗРАЧНОСТЬ

Opacity удобно использовать как gating, flicker и soft reveal. Это дёшево по вычислениям и выглядит прилично, если не превращать всё в новогоднюю гирлянду из ада.

**Креативные ручки:**

- Порог включения.
- Плавное проявление.
- Мигание по threshold.
- Release после пика.
### Dim под бит

Слой темнеет от удара.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 30);
```
### Вспышка

Появляется сильнее на ударе.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```
### Жёсткий threshold

Вкл/выкл без полутонов.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp > 10 ? 100 : 0;
```
### Soft threshold

Мягкий вход от порога.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 8;
amp < threshold ? 0 : ease(amp, threshold, 25, 0, 100);
```

---
## 📏 STROKE WIDTH — ТОЛЩИНА ОБВОДКИ

Толщина обводки хорошо работает в шейпах, typographic accents и HUD-стиле. Главное не делать обводку толще смысла.

**Креативные ручки:**

- Минимум и максимум.
- Сильнее от баса, слабее от верха.
- Связка со `Trim Paths` и `Repeaters`.
### Базовый stroke

Прямая мапа ширины.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 2, 20);
```
### Stroke + clamp

Чтобы не раздувало края.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
clamp(ease(amp, 0, 20, 2, 30), 2, 30);
```

---
## 🌈 COLOR — ЦВЕТ

Цвет лучше модулировать аккуратно: hue, saturation, brightness и alpha должны работать как команда, а не как пьяные родственники на свадьбе.

**Креативные ручки:**

- Hue shift для смены палитры.
- RGB по каналам.
- Альфа вместе с цветом.
- Palette cycling через control layer.
### RGB реакция

Меняет каналы в зависимости от амплитуды.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
r = ease(amp, 0, 20, 0.1, 1.0);
g = ease(amp, 0, 20, 0.5, 0.0);
b = 0.8;
[r, g, b, 1.0];
```
### Hue shift

Для Hue/Saturation эффектов.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 120);
```

---
## 🎭 MULTI-PROPERTY — НЕСКОЛЬКО СВОЙСТВ СРАЗУ

Правильный риг не дублирует одну и ту же аудио-логику десять раз. Он выносит расчёт в один control и раздаёт его дальше. Эстетично, быстро, не стыдно показать коллеге.

**Креативные ручки:**

- Один master slider на всё.
- Raw -> Smooth -> Gate -> Output.
- Параметрическая архитектура через null.
### Beat master

Один слайдер кормит scale, rotation и position.

```javascript

// На null:
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```
### Scale из master

Считываем только готовый control.

```javascript

null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
mapped = ease(s, 0, 100, 100, 160);
[mapped, mapped];
```
### Rotation из master

Одна логика, много outputs.

```javascript

null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
ease(s, 0, 100, 0, 20);
```

---
## 🏎️ EASING — СМЯГЧЕНИЯ

Easing делает движение менее роботским. Не потому что роботы плохие, а потому что зритель не любит видеть, как всё дёргается как у перегретого чайника.

**Креативные ручки:**

- linear = честный перевод.
- ease = мягкие края.
- easeIn / easeOut = асимметрия.
- Manual curves = полный контроль.
### linear()

Предсказуемо и быстро.

```javascript

linear(amp, 0, 20, 100, 200);
```
### ease()

Стандартный выбор для большинства случаев.

```javascript

ease(amp, 0, 20, 100, 200);
```
### easeIn / easeOut

Разный характер входа и выхода.

```javascript

easeIn(amp, 0, 20, 100, 200);
// или
easeOut(amp, 0, 20, 100, 200);
```
### Manual curve

Если нужен свой характер.

```javascript

t = clamp(amp / 20, 0, 1);
curved = t * (2 - t);
100 + curved * 100;
```

---
## 🔁 LOOP & REPEAT — ЦИКЛЫ

Петли нужны, когда движение должно жить вечно, но не выглядеть как сломанный GIF. Тут важно выбирать правильный тип повтора.

**Креативные ручки:**

- cycle для повторения.
- pingpong для туда-обратно.
- offset для нарастания.
- loopIn / loopOut для ключей.
### loopOut cycle

Повтор последнего паттерна.

```javascript

loopOut("cycle");
```
### loopOut pingpong

Возврат обратно.

```javascript

loopOut("pingpong");
```
### Синус-петля

Бесконечный органичный пульс.

```javascript

freq = 2;
amp = 50;
Math.sin(time * freq * Math.PI * 2) * amp;
```

---
## ⚡ WIGGLE + BEAT — ВИГЛ ПОД БИТ

wiggle полезен, когда нужен хаос с паспортом. Добавляешь амплитуду от бита и получаешь живое дрожание, а не случайный развал композиции.

**Креативные ручки:**

- Частота и амплитуда.
- seedRandom для уникальности.
- Отдельные оси.
- Lag / stagger для толпы.
### Базовый wiggle

Простой шум.

```javascript

wiggle(5, 20);
```
### Wiggle от амплитуды

Аудио управляет силой дрожания.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 40);
wiggle(8, wAmp);
```
### Wiggle с seed

Чтобы слои не синхронизировались как офисный митинг.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
wAmp = ease(amp, 0, 20, 0, 30);
seedRandom(index * 37, true);
wiggle(8, wAmp);
```

---
## 🎯 THRESHOLDS — ПОРОГОВЫЕ ЗНАЧЕНИЯ

Пороговые схемы полезны для триггеров, вспышек и логики вида «есть удар или нет удара». Иногда надо не плавно, а конкретно. Да, мир жесток.

**Креативные ручки:**

- Binary on/off.
- Multi-state: low / medium / high.
- Soft gate.
- Release / hold.
### Binary trigger

Вкл/выкл по threshold.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp > 12 ? 100 : 0;
```
### Multi-state

Три состояния вместо одного.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
if (amp < 5) {
  0;
} else if (amp < 15) {
  50;
} else {
  100;
}
```
### Soft gate

Мягкое включение после порога.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 8;
amp < threshold ? 0 : ease(amp, threshold, 25, 0, 100);
```

---
## 📦 UTILS — ПОЛЕЗНЫЕ ФУНКЦИИ

Это мелкие кирпичи, из которых потом строится весь риг. Нормализация, random seed, clamp, map, lerp, delay. Без них всё быстро превращается в копипасту.

**Креативные ручки:**

- normalize 0..1.
- seedRandom для повторяемого рандома.
- length() для расстояния.
- time-based patterns.
### Normalize

Привести амплитуду к 0..1.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
maxAmp = 25;
t = clamp(amp / maxAmp, 0, 1);
t;
```
### seedRandom + random

Стабильный случайный параметр на слой.

```javascript

seedRandom(index, true);
random(0, 100);
```
### Distance helper

Часто нужен для proximity-логики.

```javascript

ref = thisComp.layer("MovingDot");
pos = ref.transform.position;
center = [thisComp.width / 2, thisComp.height / 2];
length(pos, center);
```

---
## 🌊 SMOOTH MOTION — ПЛАВНОЕ ДВИЖЕНИЕ

Когда не нужен бит, но нужна живая пластика. Синусы, косинусы, орбиты, затухающие колебания, мягкие остановки. Вся цивилизация держится на `Math.PI * 2` и терпении.

**Креативные ручки:**

- Синус и косинус.
- Orbit / ellipse / Lissajous.
- Damped oscillation.
- smoothstep.
### Синус

Дыхание вверх-вниз.

```javascript

freq = 1.0;
amp = 50;
offset = Math.sin(time * freq * Math.PI * 2) * amp;
[value[0], value[1] + offset];
```
### Орбита

Круговое движение.

```javascript

freq = 0.5;
radius = 80;
cx = thisComp.width / 2;
cy = thisComp.height / 2;
angle = time * freq * Math.PI * 2;
[cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius];
```
### Затухающее колебание

Пружина, которая успокаивается.

```javascript

startTime = 1.0;
freq = 6.0;
decay = 4.0;
initAmp = 60;
t = time - startTime;
t < 0 ? value[1] : value[1] + initAmp * Math.exp(-decay * t) * Math.sin(freq * Math.PI * 2 * t);
```

---
## 🎲 RANDOM MOTION — РАНДОМНОЕ ДВИЖЕНИЕ

Рандом нужен для живости, но без контроля он моментально превращается в визуальную кашу. Поэтому важны seed, частота, задержка и диапазон.

**Креативные ручки:**

- seedRandom для уникальности.
- step random для дискретных прыжков.
- slow drift для органичного флоута.
- stagger для группы объектов.
### wiggle с редкой частотой

Медленный дрейф вместо дёрганой тряски.

```javascript

wiggle(0.2, 80);
```
### Step random

Случайное значение на интервале.

```javascript

interval = 0.5;
stepTime = Math.floor(time / interval) * interval;
seedRandom(stepTime * 1000 + index, true);
random(-50, 50);
```
### Staggered random

Каждый слой реагирует с задержкой.

```javascript

seedRandom(index * 7, true);
lag = random(0, 0.3);
audioLayer = thisComp.layer("Audio Amplitude");
delayedAmp = audioLayer.effect("Both Channels")("Slider").valueAtTime(time - lag);
ease(delayedAmp, 0, 20, 100, 160);
```

---
## 📡 INTERPOLATION — ИНТЕРПОЛЯЦИЯ МЕЖДУ ТОЧКАМИ

Интерполяция нужна, когда нужно ехать от точки A до точки B или через целый маршрут. Это не магия. Это просто аккуратная математика, которая выглядит как магия для тех, кто не хочет считать.

**Креативные ручки:**

- Линейная интерполяция.
- Smoothstep.
- Несколько точек.
- Loop по маршруту.
### lerp()

Минимальная рабочая формула.

```javascript

function lerp(a, b, t) { return a + (b - a) * t; }
t = clamp(time / 3, 0, 1);
[lerp(100, 900, t), lerp(200, 600, t)];
```
### smooth lerp

Мягкий переход.

```javascript

function smoothstep(t) { return t * t * (3 - 2 * t); }
function lerpSmooth(a, b, t) { return a + (b - a) * smoothstep(clamp(t, 0, 1)); }
t = time / 2;
[lerpSmooth(100, 800, t), lerpSmooth(500, 200, t)];
```

---
## 🔀 PROCEDURAL PATHS — ПРОЦЕДУРНЫЕ ТРАЕКТОРИИ

Процедурные пути полезны для спиралей, зигзагов, восьмёрок, пил, шагов и других форм, когда кейфреймы уже не хочется рисовать руками как пещерный художник на дедлайне.

**Креативные ручки:**

- Спираль.
- Восьмёрка.
- Zigzag / saw / step wave.
- Bouncing ball.
### Спираль

Расходящаяся траектория.

```javascript

speed = 1.0;
growth = 30;
cx = thisComp.width / 2;
cy = thisComp.height / 2;
angle = time * speed * Math.PI * 2;
radius = time * growth;
[cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius];
```
### Восьмёрка

Лемниската Бернулли.

```javascript

speed = 0.5;
a = 150;
cx = thisComp.width / 2;
cy = thisComp.height / 2;
angle = time * speed * Math.PI * 2;
scale_ = a / (1 + Math.sin(angle) * Math.sin(angle));
[cx + scale_ * Math.cos(angle), cy + scale_ * Math.sin(angle) * Math.cos(angle)];
```

---
## 🧲 FOLLOW & INERTIA — ИНЕРЦИЯ И СЛЕДОВАНИЕ

Иннерция нужна, когда объект не должен телепортироваться на новую позицию, а обязан немного подумать, прежде чем двигаться. Как взрослый человек. То есть очень медленно.

**Креативные ручки:**

- delay.
- follow leader.
- chain reaction.
- spring response.
### Delay

Простейшая инерция через прошлое значение.

```javascript

delay = 0.15;
thisLayer.transform.position.valueAtTime(time - delay);
```
### Follow leader

Слой следует за лидером.

```javascript

delay = 0.2;
leader = thisComp.layer("Leader");
leader.transform.position.valueAtTime(time - delay);
```
### Chain

Цепочка слоёв с нарастающим лагом.

```javascript

myDelay = (index - 1) * 0.08;
leader = thisComp.layer("Leader");
leader.transform.position.valueAtTime(time - myDelay);
```

---
## 🎛️ EXPRESSION CONTROLS — УПРАВЛЕНИЕ ЧЕРЕЗ UI

Самое полезное место для ручек и тумблеров. Выносишь параметры в `Slider`, `Angle`, `Point`, `Color`, `Checkbox` и перестаёшь редактировать код ради каждой мелочи.

**Креативные ручки:**

- Slider = интенсивность.
- Point = цель.
- Angle = направление.
- Checkbox = on/off.
### Slider control

Управляет энергией рига.

```javascript

ctrl = thisComp.layer("CONTROLS");
energy = ctrl.effect("Energy")("Slider");
energy;
```
### Point control

Цель для движения.

```javascript

ctrl = thisComp.layer("CONTROLS");
target = ctrl.effect("Target XY")("Point");
target;
```
### Checkbox

Вкл/выкл логики.

```javascript

ctrl = thisComp.layer("CONTROLS");
enabled = ctrl.effect("Enable")("Checkbox");
enabled ? value : value;
```

---
## 🔗 LINKING — СВЯЗЬ МЕЖДУ СЛОЯМИ

Связь между слоями превращает одиночный трюк в систему. Именно тут рождаются симметрия, зеркала, каскады, механика и пачки объектов, которые не выглядят как случайно вставленные куски картона.

**Креативные ручки:**

- Mirror.
- Inverse rotation.
- Master/slave scale.
- Distance-based opacity.
### Mirror position

Отражение относительно центра.

```javascript

leader = thisComp.layer("Element_A");
cx = thisComp.width / 2;
cy = thisComp.height / 2;
posA = leader.transform.position;
[2 * cx - posA[0], posA[1]];
```
### Inverse rotation

Вращение в противоположную сторону.

```javascript

leader = thisComp.layer("Gear_A");
-leader.transform.rotation;
```
### Distance opacity

Прозрачность зависит от расстояния до центра.

```javascript

ref = thisComp.layer("MovingDot");
pos = ref.transform.position;
cx = thisComp.width / 2;
cy = thisComp.height / 2;
dist = length(pos, [cx, cy]);
ease(dist, 0, 400, 100, 0);
```

---
## ✍️ TEXT — РАБОТА С ТЕКСТОМ

Текст в AE любит характер, но только если ты не заставляешь его делать всё подряд без дисциплины. Подпрыгивание по словам, по буквам, по строкам и сдвиги baseline обычно закрывают 90% задач.

**Креативные ручки:**

- Source Text vs Character-level.
- Per-character selectors.
- Tracking / leading / baseline.
- Word reveal / type-on.
### Source Text pulse

Самый безопасный путь: меняем не сам текст, а его параметры.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 95, 115);
[s, s];
```
### Opacity for text

Чтобы текст дышал на бит.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 70, 100);
```
### Position for text

Лёгкий подъём и отскок.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oy = ease(amp, 0, 20, 5, -10);
[value[0], value[1] + oy];
```

---
## 🖼️ SHAPE LAYERS — ШЕЙП-СЛОИ

В шейпах есть trim paths, repeater, stroke, fill, path animation и масса мест, где можно очень быстро сделать эффект, который потом все будут считать «сложным».

**Креативные ручки:**

- Trim Paths.
- Stroke Width.
- Repeater.
- Path points with expressions.
### Trim Paths

Рисование линии по биту.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```
### Shape height

Для бары-чартов и эквалайзерных столбиков.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
seedRandom(index * 13, true);
rndOffset = random(-5, 5);
h = ease(amp + rndOffset, 0, 20, 10, 200);
[value[0], h];
```

---
## 🎬 TIME — РАБОТА СО ВРЕМЕНЕМ

Когда не хочется трогать keyframes, time становится твоей универсальной шиной: циклы, интервалы, задержки, обратный ход, speed ramp и прочие красивые способы сделать просто сложнее.

**Креативные ручки:**

- time as input.
- timeOffset.
- time remap approximation.
- marker-driven timing.
### Time sine

Базовый способ сделать движение без ключей.

```javascript

freq = 1.5;
range = 50;
Math.sin(time * freq * Math.PI * 2) * range + 100;
```
### Time remap idea

Упрощённый паттерн для скорости видео.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
speedMult = ease(amp, 0, 20, 0.5, 3.0);
value + (speedMult - 1) * thisComp.frameDuration;
```

---
## 📷 CAMERA — КАМЕРА

Камера, как водится, любит быть незаметной, пока не начнёт дрожать. Хороший camera rig даёт глубину и удар, а не ощущение, что экран держит пьяный оператор.

**Креативные ручки:**

- Position shake.
- Rotation shake.
- FOV / zoom style control.
- Target follow.
### Camera shake

Базовый вибро-отклик.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 25);
w = wiggle(15, shakeAmt);
[w[0], w[1], value[2]];
```
### Rotation roll

Лёгкий завал горизонта.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
shakeAmt = ease(amp, 0, 20, 0, 2);
wiggle(12, shakeAmt);
```

---
## 💡 LIGHTS — СВЕТ

Свет хорошо работает для beat accents: intensity, cone, falloff, color temperature. Главное не устраивать сцене допрос прожектором.

**Креативные ручки:**

- Intensity.
- Color shift.
- Flicker.
- Exposure control via light rig.
### Intensity

Пульс интенсивности на ударе.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 200);
```
### Flicker

Лёгкий блеск.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
base = ease(amp, 0, 20, 0, 150);
flicker = wiggle(10, amp * 0.2);
base + flicker;
```

---
## 🌀 3D — ТРЁХМЕРНОЕ ПРОСТРАНСТВО

3D требует аккуратности: depth, order, parenting, camera, lights и scale. Тут ошибка в одном null может превратить сцену в пластилиновую кучу.

**Креативные ручки:**

- Z movement.
- Depth-based scale.
- Parallax.
- Orientation / lookAt style logic.
### 3D scale

Обычный uniform scale in 3D.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
s = ease(amp, 0, 20, 100, 150);
[s, s, s];
```
### Z push

Смещение по глубине.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
oz = ease(amp, 0, 20, 0, -200);
[value[0], value[1], value[2] + oz];
```

---
## 🔢 COUNTERS & TIMERS — СЧЁТЧИКИ

Счётчики полезны для чисел на экране, таймеров, прогресс-баров и псевдо-логики. Иногда надо не просто двигать, а ещё и считать, сколько раз мир уже сломался.

**Креативные ручки:**

- Elapsed time.
- Beat counter.
- Countdown.
- Step-based counters.
### Timer

Секунды от старта.

```javascript

start = 0;
Math.max(0, time - start);
```
### Counter by beats

Условный счётчик ударов.

```javascript

bpm = 120;
beats = time * bpm / 60;
Math.floor(beats);
```

---
## 🎨 EFFECTS — КОНКРЕТНЫЕ ЭФФЕКТЫ

Большая часть эффектов в AE отлично принимает expressions. Blur, exposure, glow, hue, levels, fill, echo, posterize time. Да, это прекрасный бардак.

**Креативные ручки:**

- Blur.
- Glow.
- Exposure.
- Hue/Saturation.
- Levels.
### Gaussian Blur

Размытие по биту.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 40);
```
### Exposure

Вспышка света.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 3);
```

---
## 📐 MASKS & TRIM PATHS — МАСКИ И ОБРЕЗКА

Маски и trim paths позволяют строить reveal, handwriting, прогресс и wipe без лишнего геморроя. Особенно полезно, когда нужно показать, а не просто махать объектом по экрану.

**Креативные ручки:**

- Mask expansion.
- Trim Start/End.
- Reveal wipe.
- Path following.
### Trim End

Появление контура по сигналу.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```

---
## 🧮 MATH PATTERNS — МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ

Базовая математика — это не скучно, это просто честно. Когда надо посчитать угол, расстояние, долю, волну или границу, лучше сделать это один раз и нормально.

**Креативные ручки:**

- clamp.
- distance.
- normalize.
- lerp.
- smoothstep.
### Clamp pattern

Защита от диких значений.

```javascript

clamp(value, 0, 100);
```
### Distance

Расстояние между точками.

```javascript

length([10, 20], [100, 200]);
```

---
## 🏗️ MASTER RIG v2 — PRODUCTION FULL RIG

Если коротко: один master null, несколько control sliders, отдельные raw/smooth/gate каналы, а дальше все свойства читают только результат. Это уже не игрушка, а production-структура.

**Креативные ручки:**

- Raw -> Smooth -> Gate.
- Energy multiplier.
- Section-specific outputs.
- One place to tune everything.
### Master flow

Схема рабочего рига.

```javascript

// Null: BEAT_MASTER
// Beat Raw -> Beat Smooth -> Beat Gate -> outputs
audioLayer = thisComp.layer("Audio Amplitude");
raw = audioLayer.effect("Both Channels")("Slider");
smooth = ease(raw, 0, 20, 0, 100);
smooth;
```
### Use in scale

Один контрол на много свойств.

```javascript

null_ = thisComp.layer("BEAT_MASTER");
s = null_.effect("Beat Smooth")("Slider");
mapped = ease(s, 0, 100, 100, 160);
[mapped, mapped];
```

---
## 🎵 FREQUENCY BANDS — ЧАСТОТНЫЕ ДИАПАЗОНЫ

Если нужен более умный audio-reactive, а не просто общий bump, разбивай реакцию на бас, середину и верх. Так картинка перестаёт реагировать на всё одинаково, что уже прогресс, почти цивилизация.

**Креативные ручки:**

- Bass for scale.
- Mids for rotation.
- Highs for flicker.
- Weighted mix.
### Band idea

Идея разнести реакцию по диапазонам через разные слои/слайдеры.

```javascript

bass = thisComp.layer("Audio Bass").effect("Slider")("Slider");
mids = thisComp.layer("Audio Mids").effect("Slider")("Slider");
highs = thisComp.layer("Audio Highs").effect("Slider")("Slider");
[bass, mids, highs];
```

---
## 👥 CROWD RIG — ТОЛПЫ И МАССИВЫ

Когда объектов много, одинаковое поведение убивает картинку. Каждому элементу нужен маленький сдвиг: seed, delay, phase, scale offset, hue offset. Иначе получишь армию клонов без души.

**Креативные ручки:**

- Unique seed per index.
- Random delay.
- Varied amplitude.
- Phase offsets.
### Random crowd scale

Разный размер у каждого слоя.

```javascript

seedRandom(index * 23, true);
s = random(60, 140);
[s, s];
```
### Crowd offset

Разброс вокруг базовой позиции.

```javascript

seedRandom(index * 17, true);
ox = random(-100, 100);
oy = random(-100, 100);
[value[0] + ox, value[1] + oy];
```

---
## ⚓ ANCHOR POINT — ТОЧКА ТРАНСФОРМАЦИИ

Anchor point нужен, когда объект должен масштабироваться, вращаться и дрожать не из центра вселенной, а из нормальной точки. Да, это часто забывают, а потом ругаются на математику.

**Креативные ручки:**

- Center anchor.
- Bottom anchor.
- Per-object offset.
### Anchor strategy

Сначала поправь anchor, потом уже двигай остальное.

```javascript

// Обычно делается вручную или через separate helper layer.
value;
```

---
## 🎞️ COMP MARKERS — МАРКЕРЫ КОМПА

Маркеры помогают строить timing, подсказки для переключений, section changes и beat landmarks. Они полезны, когда проект уже большой, а голова одна и слегка дымится.

**Креативные ручки:**

- Section markers.
- Beat markers.
- Cue markers.
### Marker timing

Можно строить переходы от маркера.

```javascript

m = thisComp.marker.key(1);
t0 = m.time;
time - t0;
```

---
## 🌊 ADVANCED WIGGLE — ПРОДВИНУТЫЙ ВИГЛ

Более умный wiggle строится не только на частоте и амплитуде, но и на октавах, multiplier, time offsets и seed. Тогда шейк перестаёт быть тупым и становится полезным.

**Креативные ручки:**

- Octaves.
- Amplitude multiplier.
- Per-axis control.
- Lagged noise.
### Octave wiggle

Более детальный шум.

```javascript

wiggle(3, 30, 3, 0.5);
```
### Axis-specific

Разный режим для X/Y.

```javascript

wx = wiggle(0.5, 60)[0];
wy = wiggle(2.0, 20)[1];
[value[0] + wx, value[1] + wy];
```

---
## 🎨 GRADIENT & COLOR ADVANCED — ЦВЕТ ПРОДВИНУТЫЙ

Градиенты, палитры и построчные shifts работают особенно хорошо в HUD, lyric videos и abstract visuals. Тут важно не превратить палитру в новогодний торт без смысла.

**Креативные ручки:**

- Gradient stop control.
- Palette cycling.
- Hue + saturation + brightness split.
### Palette shift

Простейшая идея для смены палитры.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 360);
```

---
## 🪆 PARENTING & NULL TRICKS — НУЛЛЫ И ПЭРЕНТИНГ

Null-слой это твой командный центр. Через него удобно управлять целой группой, не привязывая каждый объект к отдельной больной мысли.

**Креативные ручки:**

- Master null.
- Chain parenting.
- Offset control.
### Parent-based motion

Когда один слой управляет группой.

```javascript

master = thisComp.layer("Master Control");
s = master.transform.scale[0];
[s, s];
```

---
## 💥 VFX SNIPPETS — ГОТОВЫЕ VFX СНИППЕТЫ

Это готовые акценты: flash, glitch, shake, blur pulse, chromatic taste, micro-scale punch. Маленькие штуки, которые делают кадр живым.

**Креативные ручки:**

- Flash.
- Glitch-ish offsets.
- Blur pulse.
- Micro punch.
### Flash opacity

Короткая вспышка.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
amp > 12 ? 100 : 0;
```

---
## 🔌 EXPRESSION TO EXPRESSION — ЦЕПОЧКИ

Цепочки expressions позволяют строить сложные системы: один property считается, второй фильтрует, третий применяет. Это уже маленькая нейросеть, только без лишней рекламы.

**Креативные ручки:**

- Raw channel.
- Smooth channel.
- Gate channel.
- Output channel.
### Chain example

Raw -> smooth -> output.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
raw = audioLayer.effect("Both Channels")("Slider");
smooth = ease(raw, 0, 20, 0, 100);
smooth;
```

---
## 📊 DATA DRIVEN — ДАННЫЕ В АНИМАЦИЮ

Когда expressions питаются данными, проект становится управляемым: CSV, sliders, markers, footage metadata, external controls. Это уже почти pipeline, а не набор случайных трюков.

**Креативные ручки:**

- CSV / JSON import patterns.
- Markers as data points.
- Slider as data bus.
### Concept

Идея: разные источники данных должны кормить один риг.

```javascript

// Обычно данные заводят через slider/marker/import.
value;
```

---
## 🏃 MOTION DESIGN PATTERNS — ПАТТЕРНЫ MOTION

Вместо хаотичного набора штук лучше думать паттернами: pulse, drift, bounce, orbit, reveal, cascade, stagger, wave. Так риг легче собирать и легче объяснять человеку, который не видел его вчера ночью.

**Креативные ручки:**

- Pulse.
- Cascade.
- Wave.
- Reveal.
- Stagger.
### Pulse

Пульсирующий motion-паттерн.

```javascript

freq = 1.2;
base = 100;
range = 15;
s = base + Math.sin(time * freq * Math.PI * 2) * range;
[s, s];
```

---
## 🧰 ДИАГНОСТИКА И TROUBLESHOOTING

Когда expression не работает, не надо сразу обвинять вселенную. Сначала проверь имя слоя, тип свойства, диапазон значений, 2D/3D, parent chain, `value` и то, не поставил ли ты `Slider` на `Position` как особо смелый человек.

**Креативные ручки:**

- Проверка имён.
- Проверка диапазона.
- Проверка типов property.
- Fallback значения.
- Performance.
### Safe fallback

Когда не уверен, возвращай нормальное значение.

```javascript

try {
  audioLayer = thisComp.layer("Audio Amplitude");
  amp = audioLayer.effect("Both Channels")("Slider");
  amp;
} catch (err) {
  0;
}
```
### Clamp everywhere

Если всё летит в космос, ставь ограничители.

```javascript

clamp(value, 0, 100);
```

---
## 📋 МАСТЕР-ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ ПРОЕКТА

Перед экспортом проверь: имена слоёв, локи, range значений, 2D/3D, duration, markers, parenting, audio source, preview cache и то, не оставил ли ты случайно debug-слайдер на виду как трофей.

**Креативные ручки:**

- Все helper-слои названы одинаково.
- Amplitude layer существует.
- Ни один expression не красный.
- Риги не дублируют расчёты.

---
## 🗂️ WHAT WAS MISSING — ДОБАВЛЕННЫЕ СЕКЦИИ

В исходнике очень много сильных блоков, но для полноценной production bible не хватало нескольких вещей: attack/release, hold, envelope follower, safety guards, naming conventions и быстрых паттернов для реальных задач.

**Креативные ручки:**

- Attack / release.
- Hold / peak.
- Safety / fallback.
- Naming standard.
- Precomp strategy.
### Attack / release

Плавный вход и плавный спад.

```javascript

// Упрощённая логика: gate + soft decay
audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```
### Peak hold

Держим пик чуть дольше, чтобы удар читался.

```javascript

audioLayer = thisComp.layer("Audio Amplitude");
amp = audioLayer.effect("Both Channels")("Slider");
threshold = 12;
amp > threshold ? 100 : 0;
```
