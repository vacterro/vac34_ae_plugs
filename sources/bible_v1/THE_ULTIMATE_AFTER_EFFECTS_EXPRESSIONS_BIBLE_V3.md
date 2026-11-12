# 📘 THE ULTIMATE AFTER EFFECTS EXPRESSIONS BIBLE (V3 — ANNOTATED)
> Все 200+ expressions с описанием: что делает, какой параметр за что отвечает, что подкрутить для другого результата.

---

## 📑 TABLE OF CONTENTS
- [[#🧠 1. AUDIO DRIVEN MASTERY]]
- [[#📐 2. SCALE & PROPORTIONS]]
- [[#📍 3. POSITION & MOVEMENT]]
- [[#🔄 4. ROTATION & SWINGS]]
- [[#👻 5. OPACITY & VISIBILITY]]
- [[#🎨 6. COLOR & STYLING]]
- [[#🔁 7. LOOPS & TIME]]
- [[#⚡ 8. WIGGLE & NOISE]]
- [[#🌊 9. PHYSICS & INERTIA]]
- [[#🔗 10. LAYER SPACE & RIGGING]]

---

## 🧠 1. AUDIO DRIVEN MASTERY
> 20+ ways to process, map, and hack Audio Amplitude. Always run `Convert Audio to Keyframes` first.

### 1.1 The Master Link
> **Что делает:** Читает сырой сигнал амплитуды — базовая переменная для всех аудио-expressions. ~0 в тишине, 10–30 на ударах.
> **Применение:** Не вешай напрямую на свойство — используй как переменную в других expressions.
> **Подкрутить:** `"Left Channel"` или `"Right Channel"` вместо `"Both Channels"` — реакция только на один стерео-канал.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
amp;
```

### 1.2 Aggressive Boost
> **Что делает:** Умножает сигнал на 5 — делает реакцию ярче. Если объект едва шевелится — это первый инструмент.
> **Параметр:** `5` — множитель. `1` = без усиления, `10` = очень агрессивно.
> **Подкрутить:** `8–10` для тихих треков. `2–3` для мастеред поп. Добавь `clamp(..., 0, 100)` чтобы не вылетало.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
amp * 5;
```

### 1.3 Clamped Raw Audio (Protects from Errors)
> **Что делает:** Умножает сигнал и жёстко обрезает диапазон 0–50. Никаких выбросов, никаких вылетов.
> **Параметры:** `2` — усиление. `0` и `50` — мин/макс выхода.
> **Подкрутить:** `50` → `100` для полного диапазона. `0` → `20` — в тишине базовое значение, не ноль.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
clamp(amp * 2, 0, 50);
```

### 1.4 Linear Mapping
> **Что делает:** Преобразует амплитуду (0–20) в нужный диапазон (0–100) линейно — прямая зависимость без смягчений.
> **Параметры:** `0, 20` — входной диапазон. `0, 100` — выходной.
> **Подкрутить:** Тихий трек → уменьши `20` до `8`. Инверсия → поменяй `0, 100` на `100, 0`. Плавность → замени `linear` на `ease`.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
linear(amp, 0, 20, 0, 100);
```

### 1.5 Smoothed Mapping (Ease)
> **Что делает:** То же что linear, но с замедлением на краях — атака и затухание плавные. Органичнее смотрится на большинстве объектов.
> **Параметры:** `0, 20` — диапазон амплитуды. `0, 100` — выход.
> **Подкрутить:** Резкая атака → `easeOut`. Мягкая атака → `easeIn`. Сильнее → `100` на `200`.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 100);
```

### 1.6 Hard Attack, Soft Decay
> **Что делает:** Резко реагирует на удар, плавно затухает. Идеально под кик и бас — ощущение "удар + эхо".
> **Подкрутить:** Ещё резче → `amp * multiplier` без ease. Раньше срабатывает → уменьши `20` до `10`.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
easeOut(amp, 0, 20, 0, 100);
```

### 1.7 Soft Attack, Hard Decay
> **Что делает:** Плавно нарастает и резко обрывается. Противоположность easeOut — для пэдов и синтов с долгим сустейном.
> **Подкрутить:** Хорошо на Opacity — мягкое появление, резкое исчезновение. Комбинируй `ease` и `easeIn` на разных свойствах для контраста.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
easeIn(amp, 0, 20, 0, 100);
```

### 1.8 Stereo Split (Left Channel)
> **Что делает:** Только левый канал стерео. Если бас идёт слева — реагирует точнее чем Both Channels.
> **Подкрутить:** Вешай Left на один объект, Right на другой — стерео-реакция в пространстве сцены.
```javascript
thisComp.layer("Audio Amplitude").effect("Left Channel")("Slider");
```

### 1.9 Stereo Split (Right Channel)
> **Что делает:** Только правый канал. Хеты и тарелки часто панорамируют вправо — иногда точнее.
> **Подкрутить:** Используй вместе с 1.8 для разных осей или свойств одного объекта.
```javascript
thisComp.layer("Audio Amplitude").effect("Right Channel")("Slider");
```

### 1.10 Manual Stereo Averaging
> **Что делает:** Среднее L и R — стабильнее чем Both Channels на некоторых треках с несимметричным мастерингом.
> **Подкрутить:** `/ 1.5` вместо `/ 2` — сигнал чуть сильнее. Оберни в `ease(...)` для плавности.
```javascript
const L = thisComp.layer("Audio Amplitude").effect("Left Channel")("Slider");
const R = thisComp.layer("Audio Amplitude").effect("Right Channel")("Slider");
(L + R) / 2;
```

### 1.11 Binary Trigger (On/Off)
> **Что делает:** Мгновенное переключение: 100 если громко, 0 если тихо. Чистый строб без плавности.
> **Параметр:** `15` — порог срабатывания.
> **Подкрутить:** `25` — только на громких ударах. `5` — любой звук. `0 : 50` — в тишине полупрозрачный.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
amp > 15 ? 100 : 0;
```

### 1.12 Multi-State Trigger
> **Что делает:** Три состояния: тихо=0, средне=50, громко=100. Ступенчатый отклик — "уровни энергии".
> **Параметры:** `25` и `15` — пороги переключения.
> **Подкрутить:** Добавь четвёртый уровень: `else if (amp > 10) 25`. Смени `100, 50, 0` на `200, 100, 50` для Scale.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
if (amp > 25) 100;
else if (amp > 15) 50;
else 0;
```

### 1.13 Math.floor Stepping
> **Что делает:** Дискретные ступени — амплитуда превращается в 0, 20, 40, 60, 80, 100. Pixelated, механический отклик.
> **Параметры:** `0, 30` — вход. `0, 5` — 6 ступеней. `* 20` — шаг.
> **Подкрутить:** `5` → `3` для 4 ступеней с шагом `* 33`. Rotation: шаги по 45°.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
Math.floor(linear(amp, 0, 30, 0, 5)) * 20;
```

### 1.14 Modulo Beating
> **Что делает:** Мигает по чётности целой части амплитуды — ритмичный бинарный паттерн внутри нарастающего сигнала.
> **Подкрутить:** `% 3` — каждый третий "шаг". `100 : 30` — мигает без полного исчезновения.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
Math.floor(amp) % 2 === 0 ? 100 : 0;
```

### 1.15 Logarithmic Audio Curve
> **Что делает:** Логарифмическая кривая — тихие усиливаются, громкие пики сглаживаются. Ближе к восприятию человеческого уха.
> **Параметр:** `* 20` — масштаб. `+ 1` защищает от log(0).
> **Подкрутить:** `* 40` для большего диапазона. Оберни в `ease(...)` для дополнительного смягчения.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
Math.log(amp + 1) * 20;
```

### 1.16 Exponential Audio Curve
> **Что делает:** Подавляет тихие, резко усиливает пики. Только самые сильные удары дают заметный результат.
> **Параметры:** `/ 10` — нормализация. `2` — степень. `* 10` — масштаб выхода.
> **Подкрутить:** `2` → `3` — ещё резче реагирует на пики. Делитель `10` → `5` — раньше срабатывает.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
Math.pow(amp / 10, 2) * 10;
```

### 1.17 Delay Audio by Time
> **Что делает:** Амплитуда из прошлого — слой реагирует с задержкой 0.2 сек. Для каскадов, хвостов и эха.
> **Параметр:** `0.2` — задержка в секундах.
> **Подкрутить:** `0.05` — едва заметная задержка, но даёт плавность. `index * 0.1` — каждый слой задержан по-своему.
```javascript
const audioLayer = thisComp.layer("Audio Amplitude");
audioLayer.effect("Both Channels")("Slider").valueAtTime(time - 0.2);
```

### 1.18 Inverse Reaction (Ducking)
> **Что делает:** Инверсия — при громком звуке значение уменьшается до 0. Sidechaining: фон тихнет когда бьёт кик.
> **Параметры:** `100, 0` — инвертированный выход.
> **Подкрутить:** `100, 30` — не уходит в ноль. На Opacity фонового слоя для классического ducking.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 20, 100, 0);
```

### 1.19 Audio Speed Accumulator
> **Что делает:** Накапливает "расстояние" со скоростью пропорциональной амплитуде. Быстрее крутится когда громче.
> **Параметр:** `0, 5` — диапазон скоростей на кадр.
> **Подкрутить:** На Rotation — объект крутится быстрее под бит. `5` → `20` — агрессивнее.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const speed = linear(amp, 0, 20, 0, 5);
speed * timeToFrames(time);
```

### 1.20 Smoothstep Audio Mapping
> **Что делает:** Ручной smoothstep — плавнее чем ease(). Игнорирует шум ниже 5, насыщается к 25.
> **Параметры:** `5, 25` — рабочий диапазон (ниже 5 = тишина).
> **Подкрутить:** `5` → `0` — реагирует на любой звук. `25` → `15` — раньше насыщается. Выходной диапазон `0, 100` → `50, 200`.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const t = clamp(linear(amp, 5, 25, 0, 1), 0, 1);
const smooth = t * t * (3 - 2 * t);
linear(smooth, 0, 1, 0, 100);
```

---

## 📐 2. SCALE & PROPORTIONS

### 2.1 Basic Uniform Pump
> **Что делает:** Равномерно увеличивает с 100% до 130% на ударе. Классический beat-pump.
> **Параметры:** `5, 25` — диапазон амплитуды. `100, 130` — базовый и максимальный размер.
> **Подкрутить:** `100, 160` — агрессивнее. `100, 110` — мягкое дыхание. `easeOut` для резкой атаки. `[s, s*0.9]` для лёгкого squash.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = ease(amp, 5, 25, 100, 130);
[s, s];
```

### 2.2 Additive Scale (Keeps original)
> **Что делает:** Добавляет boost от амплитуды к кейфреймовому значению. Кейфреймы сохраняются.
> **Параметр:** `0, 40` — сколько процентов добавляется на максимуме.
> **Подкрутить:** `0, 20` — мягче. `0, 80` — агрессивнее. Идеально когда анимация Scale уже есть и хочешь бит сверху.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const boost = ease(amp, 0, 20, 0, 40);
value + [boost, boost];
```

### 2.3 Proportional Multiplication
> **Что делает:** Умножает текущий Scale на множитель 1–1.5. Сохраняет пропорции даже если scale не 100%.
> **Параметр:** `1, 1.5` — множитель. `0.5, 1.5` — сначала уменьшается потом растёт.
> **Подкрутить:** `1, 1.2` — мягче. Хорош когда объект уже масштабирован кейфреймами.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const mult = ease(amp, 0, 20, 1, 1.5);
[value[0] * mult, value[1] * mult];
```

### 2.4 Squash and Stretch (Y Squash)
> **Что делает:** На удар расширяется по X и сжимается по Y — классика Диснея. Для мячей, ударов, хитов.
> **Параметры:** `sx 100→140` — ширина. `sy 100→70` — высота.
> **Подкрутить:** `sx 100→120, sy 100→85` — мягкий squash. `sx 100→180, sy 100→50` — экстремальный cartoon. Инвертируй оси для вытягивания вверх.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const sx = ease(amp, 5, 25, 100, 140);
const sy = ease(amp, 5, 25, 100, 70);
[sx, sy];
```

### 2.5 Squash and Stretch (X Squash)
> **Что делает:** Сжимается по X, вытягивается по Y — объект "подпрыгивает" на удар.
> **Подкрутить:** Добавь смещение по Y вверх (`value[1] - boost`) чтобы основание оставалось на месте.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const sx = ease(amp, 5, 25, 100, 60);
const sy = ease(amp, 5, 25, 100, 150);
[sx, sy];
```

### 2.6 Inverse Scale Reaction (Shrink on beat)
> **Что делает:** Уменьшается на ударе с 100% до 50%. Ducking для масштаба — фон сжимается.
> **Подкрутить:** `100, 80` — небольшое сжатие. `100, 0` — исчезает. Для фоновых элементов уступающих место главному.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = ease(amp, 0, 25, 100, 50);
[s, s];
```

### 2.7 3D Uniform Scale
> **Что делает:** Scale по всем трём осям для 3D слоёв. Без третьего значения Z не масштабируется.
> **Подкрутить:** `[s, s, s * 2]` — Z вдвое сильнее, "толстеет" в глубину.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = ease(amp, 0, 20, 100, 200);
[s, s, s];
```

### 2.8 3D Depth Punch (Z-Scale Only)
> **Что делает:** Только Z-ось — объект "вылетает" навстречу камере. X и Y не меняются.
> **Параметр:** `100, 500` — Z масштаб до 5x.
> **Подкрутить:** `[value[0], value[1], z * 0.5]` — мягче. Комбинируй с camera shake для взрыва.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const z = ease(amp, 0, 25, 100, 500);
[value[0], value[1], z];
```

### 2.9 Index-Based Scale Offset (Crowd effect)
> **Что делает:** Каждый слой масштабируется до разного максимума — чем выше index, тем больше. "Стадный" эффект.
> **Параметр:** `index * 5` — шаг между слоями.
> **Подкрутить:** `index * 10` — заметнее разница. `150 - (index * 5)` — инверсия: первые больше.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = ease(amp, 0, 20, 100, 150 + (index * 5));
[s, s];
```

### 2.10 Audio Triggered Pop-in
> **Что делает:** 100% при громком звуке, 0% при тихом. Появляется только на ударах.
> **Параметр:** `15` — порог.
> **Подкрутить:** `amp > 15 ? ease(amp, 15, 25, 80, 100) : 0` — появляется плавно от порога.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = amp > 15 ? 100 : 0;
[s, s];
```

### 2.11 Constant Breathing Scale
> **Что делает:** Постоянное синусоидальное пульсирование без аудио. Органично, бесконечно.
> **Параметры:** `freq = 2` — циклов/сек. `amp = 10` — диапазон ±%.
> **Подкрутить:** `freq = 0.5` — глубокое дыхание. `amp = 30` — сильнее. `+ index * 0.5` к аргументу sin — вразнобой.
```javascript
const freq = 2;
const amp = 10;
const s = 100 + Math.sin(time * freq * Math.PI * 2) * amp;
[s, s];
```

### 2.12 Breathing Audio Multiplier
> **Что делает:** Синусоида × амплитуда — объект дышит сильнее когда громче музыка.
> **Параметр:** `* 5` — скорость колебания. Диапазон = audioAmp.
> **Подкрутить:** `Math.sin(time * 2)` — медленнее. `Math.sin(time * 10)` — быстрая дрожь.
```javascript
const audioAmp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const s = 100 + Math.sin(time * 5) * audioAmp;
[s, s];
```

### 2.13 Wiggle Scale (Maintains aspect ratio)
> **Что делает:** Scale шумит через wiggle — X и Y синхронно, соотношение сторон не нарушается.
> **Параметр:** `wiggle(5, 30)` — 5 раз/сек, ±30%.
> **Подкрутить:** `wiggle(1, 60)` — редкие большие прыжки. `wiggle(20, 5)` — мелкая быстрая дрожь.
```javascript
const w = wiggle(5, 30);
const s = value[0] + (w[0] - value[0]);
[s, s];
```

### 2.14 Wiggle Only on X Width
> **Что делает:** Только ширина шумит, высота зафиксирована.
> **Подкрутить:** `wiggle(1, 50)` — медленные волны. `wiggle(15, 10)` — быстрое дрожание. Аудио: замени `50` на `ease(amp, 0,20, 0,80)`.
```javascript
const w = wiggle(4, 50);
[w[0], value[1]];
```

### 2.15 Wiggle Only on Y Height
> **Что делает:** Только высота шумит, ширина зафиксирована.
> **Подкрутить:** Для "дышащих" полосок, прогресс-баров. `wiggle(0.3, 100)` — редкие всплески высоты.
```javascript
const w = wiggle(4, 50);
[value[0], w[1]];
```

### 2.16 Delay Leader Scale
> **Что делает:** Копирует Scale лидера с задержкой по index — волна масштабирования по цепочке.
> **Параметр:** `delay = 0.1` — секунд между слоями.
> **Подкрутить:** `0.05` — быстрая волна. `0.3` — медленная. Замени `"Leader"` на имя своего слоя.
```javascript
const leader = thisComp.layer("Leader");
const delay = 0.1;
leader.scale.valueAtTime(time - (index * delay));
```

### 2.17 Random Scale on Each Frame
> **Что делает:** Каждый кадр случайный Scale 50%–150%. Стробоскопический размер.
> **Подкрутить:** `random(90, 110)` — мелкое дрожание. `seedRandom(index, true)` — фиксированный размер на каждом слое.
```javascript
const s = random(50, 150);
[s, s];
```

### 2.18 Stepped Random Scale
> **Что делает:** Scale прыгает каждые `holdTime` секунд и держится — ступенчатые дискретные прыжки.
> **Параметр:** `holdTime = 0.5`. `80, 120` — диапазон.
> **Подкрутить:** `holdTime = 60/120` — прыжок каждый бит при 120 BPM. `random(50, 200)` — шире диапазон.
```javascript
const holdTime = 0.5;
seedRandom(Math.floor(time / holdTime), true);
const s = random(80, 120);
[s, s];
```

### 2.19 Elastic Rubber Scale (Inertial Pull)
> **Что делает:** Scale "тянется" к цели с инерцией — не прыгает мгновенно, плавно догоняет. Эффект резинки.
> **Параметр:** `0.15` — скорость притяжения (0.01 = медленно, 0.5 = быстро).
> **Подкрутить:** `0.05` — тягучая резинка. `0.3` — упругая. ⚠️ Нужен стартовый кейфрейм — иначе зациклится.
```javascript
const target = linear(thisComp.layer("Audio").effect("Both")("Slider"), 0, 20, 100, 150);
const current = value[0];
const spring = current + (target - current) * 0.15;
[spring, spring];
```

### 2.20 Stereo Separated Scaling
> **Что делает:** X = левый канал, Y = правый. Объект растягивается асимметрично от стерео-панорамы.
> **Подкрутить:** `ease(L,...) * 0.5` — Y вдвое слабее. Инверсия одного: `ease(L, 0,20, 150, 100)` — левый сжимает.
```javascript
const L = thisComp.layer("Audio Amplitude").effect("Left Channel")("Slider");
const R = thisComp.layer("Audio Amplitude").effect("Right Channel")("Slider");
const sx = ease(L, 0, 20, 100, 150);
const sy = ease(R, 0, 20, 100, 150);
[sx, sy];
```

---

## 📍 3. POSITION & MOVEMENT

### 3.1 Vertical Audio Jump (Y-Axis)
> **Что делает:** Прыжок ВВЕРХ на удар (отрицательный Y = вверх в AE). В тишине на месте.
> **Параметры:** `10, 30` — диапазон амплитуды. `-100` — высота прыжка.
> **Подкрутить:** `-200` — выше. `+100` — прыгает вниз. `easeOut` — резкий удар, плавный возврат.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const jump = ease(amp, 10, 30, 0, -100);
[value[0], value[1] + jump];
```

### 3.2 Horizontal Audio Dash (X-Axis)
> **Что делает:** Рывок вправо по X на удар.
> **Параметры:** `0, 100` — дистанция.
> **Подкрутить:** `-100` — влево. Добавь wiggle на Y — не строго горизонтальное.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const dash = ease(amp, 10, 30, 0, 100);
[value[0] + dash, value[1]];
```

### 3.3 Diagonal Audio Kick
> **Что делает:** Диагональный рывок — вправо и вверх одновременно. Динамичнее чем по одной оси.
> **Параметр:** `move = 50` — дистанция.
> **Подкрутить:** `[value[0] + move, value[1] + move]` — вправо-вниз. `move * 2` на одной оси — другой угол.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const move = ease(amp, 5, 25, 0, 50);
[value[0] + move, value[1] - move];
```

### 3.4 Audio Driven Shake (Vibration)
> **Что делает:** Синусоидальный шейк — трясёт объект на удар. Детерминированный (не случайный как wiggle).
> **Параметры:** `shakeAmt` — размах. `freq = 15` — Гц колебания.
> **Подкрутить:** `freq = 8` — медленнее видны волны. `freq = 30` — быстрая мелкая дрожь. Убери `oy` — shake только по X.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const shakeAmt = ease(amp, 10, 30, 0, 50);
const freq = 15;
const ox = Math.sin(time * freq * Math.PI * 2) * shakeAmt;
const oy = Math.cos(time * freq * Math.PI * 2 * 0.7) * shakeAmt;
value + [ox, oy];
```

### 3.5 Stereo Drift (L/R Pan)
> **Что делает:** Дрейф влево/вправо по стерео-балансу. Левый громче = влево, правый = вправо.
> **Параметр:** `-150, 150` — максимальный сдвиг.
> **Подкрутить:** `-300, 300` — экстремально. Для визуализаторов где элементы "живут" в стерео-пространстве.
```javascript
const L = thisComp.layer("Audio Amplitude").effect("Left Channel")("Slider");
const R = thisComp.layer("Audio Amplitude").effect("Right Channel")("Slider");
const pan = ease(R - L, -20, 20, -150, 150);
[value[0] + pan, value[1]];
```

### 3.6 Time-Based Orbit
> **Что делает:** Вращение по окружности вокруг центра компа без аудио — чисто процедурное.
> **Параметры:** `radius = 250` — радиус. `speed = 1.5` — оборотов/сек.
> **Подкрутить:** `speed = 0.1` — медленно. Замени `[thisComp.width/2, thisComp.height/2]` на позицию другого слоя — вращается вокруг него.
```javascript
const center = [thisComp.width/2, thisComp.height/2];
const radius = 250;
const speed = 1.5;
const x = center[0] + Math.cos(time * speed * Math.PI * 2) * radius;
const y = center[1] + Math.sin(time * speed * Math.PI * 2) * radius;
[x, y];
```

### 3.7 Audio-Reactive Orbit Radius
> **Что делает:** Орбита расширяется на удар — объект отлетает от центра и возвращается.
> **Параметры:** `100, 300` — мин и макс радиус.
> **Подкрутить:** `50, 500` — экстремально. Добавь реакцию на `speed` — ускоряется под бит.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const radius = ease(amp, 0, 25, 100, 300);
const speed = 1;
const x = value[0] + Math.cos(time * speed * Math.PI * 2) * radius;
const y = value[1] + Math.sin(time * speed * Math.PI * 2) * radius;
[x, y];
```

### 3.8 Random Jump on Beat
> **Что делает:** На удар прыжок в случайном направлении — дистанция пропорциональна амплитуде.
> **Параметр:** `Math.floor(time * 5)` — 5 обновлений/сек.
> **Подкрутить:** `time * 2` — реже. `amp * 10` — прыжки больше. `clamp` на результат — не улетает за экран.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
seedRandom(Math.floor(time * 5), true);
const jumpX = random(-1, 1) * amp * 5;
const jumpY = random(-1, 1) * amp * 5;
value + [jumpX, jumpY];
```

### 3.9 Snap to Grid (Pixel Art / Retro)
> **Что делает:** Позиция "щёлкает" по сетке — пиксельный ретро-стиль.
> **Параметр:** `gridSize = 50` — шаг сетки.
> **Подкрутить:** `gridSize = 10` — мелкая сетка. `gridSize = 200` — грубая. Комбинируй с 3.8 — случайные прыжки строго по сетке.
```javascript
const gridSize = 50;
const x = Math.round(value[0] / gridSize) * gridSize;
const y = Math.round(value[1] / gridSize) * gridSize;
[x, y];
```

### 3.10 Sub-Pixel Anti-Aliasing Fix
> **Что делает:** Округляет координаты до целых пикселей — убирает плавающее размытие на чётких краях.
> **Подкрутить:** Применяй на иконках, пикселях, тексте. Не нужно для органичной анимации.
```javascript
[Math.round(value[0]), Math.round(value[1])];
```

### 3.11 Continuous Drift (Speed)
> **Что делает:** Постоянное движение с фиксированной скоростью. Как конвейер.
> **Параметры:** `speedX = 100` — пикселей/сек. `speedY = 50`.
> **Подкрутить:** `speedX = -200` — влево. `speedY = 0` — только горизонталь. `% thisComp.width` — бесконечный цикл.
```javascript
const speedX = 100;
const speedY = 50;
value + [speedX * time, speedY * time];
```

### 3.12 Parallax Follow (Depth simulation)
> **Что делает:** Движется с "камерой" но медленнее — параллакс и глубина.
> **Параметр:** `depthFactor = 0.5` — насколько "дальше" (0.1 = очень далеко).
> **Подкрутить:** `0.2` — далёкий фон. `0.8` — близко. Null управляемый мышью — интерактивный параллакс.
```javascript
const cam = thisComp.layer("Camera Tracker");
const depthFactor = 0.5;
value + (cam.position - [thisComp.width/2, thisComp.height/2]) * depthFactor;
```

### 3.13 3D Z-Depth Audio Punch
> **Что делает:** 3D слой летит навстречу камере по Z на удар — "пробивает" экран.
> **Параметр:** `-500` — дистанция (отрицательный Z = ближе к камере).
> **Подкрутить:** `-200` — мягче. `-1000` — экстремально. Комбинируй с Scale для усиления.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const z = ease(amp, 0, 30, 0, -500);
[value[0], value[1], value[2] + z];
```

### 3.14 Sinewave Pathing (Dolphin motion)
> **Что делает:** Движется вправо и волнообразно по Y — как дельфин.
> **Параметры:** `speedX = 200` — горизонталь. `freqY = 2` — частота. `ampY = 150` — высота волны.
> **Подкрутить:** `freqY = 5` — частая мелкая волна. `speedX = 0` — качается на месте вертикально.
```javascript
const speedX = 200;
const freqY = 2;
const ampY = 150;
const x = value[0] + (time * speedX);
const y = value[1] + (Math.sin(time * freqY * Math.PI * 2) * ampY);
[x, y];
```

### 3.15 Hovering / Floating Loop
> **Что делает:** Мягкое вертикальное парение. Идеально для иконок, кнопок, персонажей на паузе.
> **Параметры:** `freq = 1` — циклов/сек. `amp = 20` — высота.
> **Подкрутить:** `freq = 0.5` — медленно. `+ index * Math.PI * 0.5` к sin — вразнобой.
```javascript
const freq = 1;
const amp = 20;
const y = Math.sin(time * freq * Math.PI * 2) * amp;
value + [0, y];
```

### 3.16 Figure 8 Motion (Infinity loop)
> **Что делает:** Траектория по форме символа ∞. Плавная, непрерывная.
> **Параметры:** `scale = 200` — размер. `speed = 2` — скорость.
> **Подкрутить:** `scale = 100` — меньше. `speed = 0.5` — медленнее. Измени формулу на `Math.sin(t * 2)` — лемнискат Бернулли.
```javascript
const scale = 200;
const speed = 2;
const t = time * speed;
const x = Math.sin(t) * scale;
const y = Math.sin(t) * Math.cos(t) * scale;
value + [x, y];
```

### 3.17 Step/Stairs Motion
> **Что делает:** Дискретные шаги — прыгает на `stepDistance` пикселей каждые `stepTime` секунд.
> **Параметры:** `stepTime = 1`. `stepDistance = 100`.
> **Подкрутить:** `stepTime = 60/120` — шаг каждый бит при 120 BPM. По Y или в минус для других направлений.
```javascript
const stepTime = 1;
const stepDistance = 100;
const currentStep = Math.floor(time / stepTime);
[value[0] + (currentStep * stepDistance), value[1]];
```

### 3.18 Hard Limit Bounds (Clamp Position)
> **Что делает:** Жёсткие границы — объект не может выйти за заданный прямоугольник.
> **Параметры:** `200, 1720` — X границы. `200, 880` — Y границы.
> **Подкрутить:** `0, thisComp.width` / `0, thisComp.height` — границы компа.
```javascript
const x = clamp(value[0], 200, 1720);
const y = clamp(value[1], 200, 880);
[x, y];
```

### 3.19 Wiggle X and Drift Y
> **Что делает:** Шатается по X и плавно поднимается — как пузырь или дым.
> **Параметр:** `time * 50` — скорость подъёма (пикс/сек).
> **Подкрутить:** `time * 20` — медленнее. `+ time * 50` — опускается вниз.
```javascript
const wx = wiggle(3, 100)[0];
const dy = value[1] - (time * 50);
[wx, dy];
```

### 3.20 Distance-Based Repel (Avoid Mouse/Null)
> **Что делает:** Отталкивается от слоя "Cursor" — чем ближе, тем сильнее отталкивание.
> **Параметры:** `maxDist = 200` — радиус. `force = 100` — сила.
> **Подкрутить:** `maxDist = 400` — шире зона. Замени `value - mouse` на `mouse - value` — притягивает.
```javascript
const mouse = thisComp.layer("Cursor").position;
const maxDist = 200;
const force = 100;
const dist = length(mouse, value);
if (dist < maxDist) {
    const dir = normalize(value - mouse);
    const repel = ease(dist, 0, maxDist, force, 0);
    value + (dir * repel);
} else {
    value;
}
```

---

## 🔄 4. ROTATION & SWINGS

### 4.1 Direct Audio Rotation
> **Что делает:** Поворот вправо на удар — от 0° до 45°.
> **Параметры:** `0, 20` — амплитуда. `0, 45` — угол.
> **Подкрутить:** `-45, 45` — качается туда-сюда. `0, 180` — полуоборот. `easeOut` — резкий, плавный возврат.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 20, 0, 45);
```

### 4.2 Bi-directional Audio Rocking
> **Что делает:** Качается от -20° до +20° — в тишине нейтрально, на ударе отклоняется.
> **Параметры:** `5, 25` — амплитуда. `-20, 20` — угол.
> **Подкрутить:** `-45, 45` — шире. Убери минус — только в одну сторону.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 5, 25, -20, 20);
```

### 4.3 Accumulating Spin (RPM)
> **Что делает:** Непрерывное вращение с заданным RPM. Точный контроль — как мотор.
> **Параметр:** `rpm = 30`. `60` = 1 оборот/сек.
> **Подкрутить:** `rpm = -30` — обратная сторона. Используй Slider Control для управления в реальном времени.
```javascript
const rpm = 30;
(time * rpm * 360) / 60;
```

### 4.4 Audio Driven Accumulating Spin
> **Что делает:** Скорость зависит от амплитуды — чем громче, тем быстрее крутится. Накапливается.
> **Параметр:** `0, 10` — скорость (градусов/кадр).
> **Подкрутить:** `5, 10` — всегда крутится, ускоряется на ударе. `easeOut` — резкий разгон.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const speed = ease(amp, 0, 20, 0, 10);
value + (speed * timeToFrames(time));
```

### 4.5 Sine Wave Pendulum
> **Что делает:** Маятниковое качание — плавно ±45°.
> **Параметры:** `freq = 1.5` — качаний/сек. `maxAngle = 45`.
> **Подкрутить:** `freq = 0.3` — медленный. `maxAngle = 90` — широкое качание. `freq = 4` — быстрое дрожание.
```javascript
const freq = 1.5;
const maxAngle = 45;
Math.sin(time * freq * Math.PI * 2) * maxAngle;
```

### 4.6 Decay Swing (Swings and settles)
> **Что делает:** Маятник с затуханием — раскачивается и останавливается. Физически правдоподобно.
> **Параметры:** `freq = 3`, `decay = 0.5`, `maxAngle = 90`.
> **Подкрутить:** `decay = 2` — быстро успокаивается. `decay = 0.1` — долго качается. Перезапускай по маркеру.
```javascript
const freq = 3;
const decay = 0.5;
const maxAngle = 90;
Math.cos(time * freq * Math.PI * 2) * maxAngle / Math.exp(decay * time);
```

### 4.7 Audio Pendulum (Swings wider on beat)
> **Что делает:** Маятник чья амплитуда зависит от громкости.
> **Параметры:** `10, 60` — диапазон амплитуды качания. `freq = 2`.
> **Подкрутить:** `5, 90` — от едва заметного до полного оборота.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const currentAngle = ease(amp, 0, 30, 10, 60);
Math.sin(time * 2 * Math.PI * 2) * currentAngle;
```

### 4.8 Wiggle Rotation Only
> **Что делает:** Случайное дрожание угла.
> **Параметры:** `5` — раз/сек. `15` — диапазон.
> **Подкрутить:** `wiggle(1, 45)` — редкие большие повороты. `wiggle(5, ease(amp, 0,20, 0,30))` — от аудио.
```javascript
wiggle(5, 15);
```

### 4.9 Clock Hands (Second Hand Stepping)
> **Что делает:** Точная секундная стрелка — прыгает на 6° каждую секунду.
> **Параметр:** `steps = 60` — делений.
> **Подкрутить:** `steps = 12` — часовая стрелка (30°). `Math.floor(time * 10)` — 10 раз/сек.
```javascript
const steps = 60;
Math.floor(time) * (360 / steps);
```

### 4.10 Clock Hands (Smooth Minute Hand)
> **Что делает:** Плавное вращение — оборот за 60 секунд.
> **Подкрутить:** `/ 3600` — часовая. `/ 10` — быстро. `* -1` — против часовой.
```javascript
time * (360 / 60);
```

### 4.11 Auto-Orient to Motion Path (2D)
> **Что делает:** Автоматически поворачивается лицом в направлении движения.
> **Подкрутить:** `+ 90` — перпендикулярно движению. `+ 180` — лицом назад.
```javascript
const v = velocity;
radiansToDegrees(Math.atan2(v[1], v[0]));
```

### 4.12 LookAt Target (Turret logic)
> **Что делает:** Всегда смотрит на слой "Target" — как башня танка или стрелка компаса.
> **Подкрутить:** `+ 90` — поворот на 90° от направления. Null управляемый мышью — интерактивный прицел.
```javascript
const target = thisComp.layer("Target").position;
const p = position;
const delta = target - p;
radiansToDegrees(Math.atan2(delta[1], delta[0]));
```

### 4.13 Inverse Parent Rotation (Ferris Wheel Bucket)
> **Что делает:** Дочерний объект всегда горизонтален — как кабинка колеса обозрения.
> **Подкрутить:** `* 0.5` — полукомпенсация. Для текста на вращающихся объектах.
```javascript
value - parent.transform.rotation;
```

### 4.14 Gear Ratio (Linked Rotation)
> **Что делает:** Шестерня вращается противоположно и в `ratio` раз быстрее главной.
> **Параметр:** `ratio = 2.5`.
> **Подкрутить:** `ratio = 1` — та же скорость, обратная сторона. `ratio = -2.5` — та же сторона, быстрее.
```javascript
const mainGear = thisComp.layer("Main Gear").transform.rotation;
const ratio = 2.5;
mainGear * -ratio;
```

### 4.15 Random Angle per Duplicate (Index)
> **Что делает:** Каждый скопированный слой — уникальный угол. Фиксированный, не меняется.
> **Подкрутить:** `random(0, 90)` — первый квадрант. `random(-15, 15)` — разброс вокруг нуля.
```javascript
seedRandom(index, true);
random(0, 360);
```

### 4.16 Wheel Roll Equation (Accurate rolling)
> **Что делает:** Колесо вращается пропорционально пути — без скольжения.
> **Подкрутить:** По Y — замени `position[0]` на `position[1]`. `* -1` — обратное направление.
```javascript
const radius = thisComp.layer("Wheel").sourceRectAtTime().width / 2;
const dist = position[0];
(dist / (2 * Math.PI * radius)) * 360;
```

### 4.17 Bank on Turn (Airplane Roll)
> **Что делает:** Наклоняется в сторону поворота — как самолёт в вираже.
> **Параметр:** `factor = 0.05` — сила крена.
> **Подкрутить:** `0.1` — сильнее. `clamp(..., -45, 45)` — не опрокидывается.
```javascript
const vx = position.velocity[0];
const factor = 0.05;
value + (vx * factor);
```

### 4.18 Sine Wave Bank (Fish tail)
> **Что делает:** Виляет синусоидой — быстрее движется, сильнее виляет.
> **Подкрутить:** `Math.sin(time * 5)` — медленнее. `ease(Math.abs(v), 0, 200, 0, 30)` — меньший диапазон скорости.
```javascript
const v = velocity[0];
const amp = ease(Math.abs(v), 0, 500, 0, 45);
Math.sin(time * 10) * amp;
```

### 4.19 Stereo Audio DJ Spin
> **Что делает:** Крутится влево когда L громче, вправо когда R громче.
> **Параметры:** `-90, 90` — диапазон.
> **Подкрутить:** `-180, 180` — полный оборот. Для виниловой пластинки или DJ-эффектов.
```javascript
const L = thisComp.layer("Audio Amplitude").effect("Left Channel")("Slider");
const R = thisComp.layer("Audio Amplitude").effect("Right Channel")("Slider");
ease(R - L, -30, 30, -90, 90);
```

### 4.20 Random Flip (Coin Toss)
> **Что делает:** Случайно переворачивается на 0° или 180° — как монета.
> **Параметр:** `tossSpeed = 2` — раз/сек.
> **Подкрутить:** `tossSpeed = 0.5` — медленно. Четыре ориентации: `Math.floor(random(0,4)) * 90`.
```javascript
const tossSpeed = 2;
seedRandom(Math.floor(time * tossSpeed), true);
random(1) > 0.5 ? 0 : 180;
```

---

## 👻 5. OPACITY & VISIBILITY

### 5.1 Basic Audio Strobe
> **Что делает:** Прозрачность от амплитуды — в тишине невидим, на ударе виден.
> **Параметры:** `10, 30` — амплитуда. `0, 100` — прозрачность.
> **Подкрутить:** `50, 100` — в тишине полупрозрачный. `easeOut` — резко появляется, плавно гаснет.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 10, 30, 0, 100);
```

### 5.2 Audio Ducking (Darkens on beat)
> **Что делает:** На ударе становится невидимым — фон "уходит".
> **Подкрутить:** `100, 20` — не исчезает полностью. На фоновый слой для sidechaining.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 10, 30, 100, 0);
```

### 5.3 Hard Strobe Gate (Flash)
> **Что делает:** Либо 100% либо 0% — без промежутков. Жёсткий строб.
> **Параметр:** `20` — порог.
> **Подкрутить:** `15` — чаще. `30` — только на громких. С Mode=Add — световая вспышка.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
amp > 20 ? 100 : 0;
```

### 5.4 Alternating Index Strobe
> **Что делает:** Чётные и нечётные слои мигают в противофазе — шахматный паттерн.
> **Подкрутить:** `index % 3 === 0` — каждый третий. `100 : 30` — нечётные не исчезают.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
if (amp > 20) {
    index % 2 === 0 ? 100 : 0;
} else {
    index % 2 === 0 ? 0 : 100;
}
```

### 5.5 Sine Wave Pulse (Breathing LED)
> **Что делает:** Прозрачность пульсирует 0%–100% — как светодиод или неон.
> **Параметры:** `freq = 1`, `amp = 50` (50±50 = 0..100).
> **Подкрутить:** `freq = 4` — быстрое мигание. `30 + sin * 30` — от 0% до 60%.
```javascript
const freq = 1;
const amp = 50;
50 + Math.sin(time * freq * Math.PI * 2) * amp;
```

### 5.6 Wiggle Flicker
> **Что делает:** Быстрый хаотичный мерцающий свет — сломанный флуоресцент.
> **Параметры:** `20` — раз/сек. `100` — диапазон.
> **Подкрутить:** `wiggle(5, 30)` — медленное мерцание. `clamp(..., 20, 100)` — никогда не гаснет.
```javascript
wiggle(20, 100);
```

### 5.7 Neon Broken Bulb (Random Drops)
> **Что делает:** Горит, иногда случайно проваливается — неисправная неоновая вывеска.
> **Параметр:** `> 95` — вероятность провала (5%).
> **Подкрутить:** `> 80` — провалов больше (20%). `> 99` — редкие короткие моргания.
```javascript
const flick = random(100);
flick > 95 ? random(0, 50) : 100;
```

### 5.8 Audio Modulated Broken Bulb
> **Что делает:** При громкой музыке стабильно горит, в тишине мерцает.
> **Параметр:** `threshold = 15`.
> **Подкрутить:** `> 80` — чаще мерцает в тишине. Для атмосферных сцен.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const threshold = 15;
if (amp > threshold) 100;
else random(100) > 90 ? random(0, 50) : 100;
```

### 5.9 Camera Proximity Fade (Z-Depth)
> **Что делает:** 3D слой исчезает когда камера далеко — туман/видимость.
> **Параметры:** `500, 1500` — дистанция затухания.
> **Подкрутить:** `200, 800` — туман ближе. Инверсия `0, 100` — появляется вдали.
```javascript
const cam = thisComp.layer("Camera 1").position;
const me = toWorld(anchorPoint);
const dist = length(cam, me);
ease(dist, 500, 1500, 100, 0);
```

### 5.10 Object Proximity Fade (Reveal)
> **Что делает:** Виден только когда "Cursor" рядом.
> **Параметры:** `0, 300` — радиус видимости.
> **Подкрутить:** `0, 600` — шире. Инверсия — прячется при приближении.
```javascript
const cursor = thisComp.layer("Cursor").position;
const dist = length(cursor, position);
ease(dist, 0, 300, 100, 0);
```

### 5.11 Blink / Blinking Cursor
> **Что делает:** Регулярное мигание — как курсор в текстовом редакторе.
> **Параметр:** `blinkRate = 2` — миганий/сек.
> **Подкрутить:** `? 80 : 20` — между 20% и 80%, не полностью.
```javascript
const blinkRate = 2;
Math.floor(time * blinkRate) % 2 === 0 ? 100 : 0;
```

### 5.12 Soft Blink (Sine)
> **Что делает:** Плавное мигание через абсолютный синус — без резких переходов.
> **Параметр:** `freq = 2`.
> **Подкрутить:** `* 80` — не доходит до 100%. Для световых полос и неона.
```javascript
const freq = 2;
Math.abs(Math.sin(time * freq * Math.PI)) * 100;
```

### 5.13 Checkbox Visibility Switch
> **Что делает:** Чекбокс на CTRL включает/выключает видимость.
> **Подкрутить:** `cb == 1 ? 50 : 0` — включённый полупрозрачный.
```javascript
const cb = thisComp.layer("CTRL").effect("Checkbox Control")("Checkbox");
cb == 1 ? 100 : 0;
```

### 5.14 Fade In over Time
> **Что делает:** Плавное появление от inPoint за заданное время.
> **Параметр:** `fadeDuration = 2`.
> **Подкрутить:** `0.3` — быстро. `5` — медленно. `easeIn` — медленный старт, быстрый финиш.
```javascript
const fadeDuration = 2;
ease(time, inPoint, inPoint + fadeDuration, 0, 100);
```

### 5.15 Fade Out over Time
> **Что делает:** Плавное исчезновение перед outPoint.
> **Подкрутить:** `0.5` — быстро. Комбинируй с 5.14 для полного fade in/out.
```javascript
const fadeDuration = 2;
ease(time, outPoint - fadeDuration, outPoint, 100, 0);
```

### 5.16 Fade In and Out (Automatic bounds)
> **Что делает:** Автоматический fade на обоих концах слоя.
> **Параметр:** `fade = 1` — секунд каждый fade.
> **Подкрутить:** `0.3` — быстрые переходы. `3` — долгие. Идеален для любого слоя.
```javascript
const fade = 1;
if (time < inPoint + fade) {
    ease(time, inPoint, inPoint + fade, 0, 100);
} else if (time > outPoint - fade) {
    ease(time, outPoint - fade, outPoint, 100, 0);
} else {
    100;
}
```

### 5.17 Speed-Based Motion Blur Fade
> **Что делает:** Прозрачнее при быстром движении — имитация motion blur.
> **Параметр:** `0, 1000` — диапазон скоростей.
> **Подкрутить:** `ease(v, 0, 1000, 100, 30)` — не исчезает полностью.
```javascript
const v = length(position.velocity);
ease(v, 0, 1000, 100, 0);
```

### 5.18 Audio Step Thresholds (3 levels)
> **Что делает:** Три уровня прозрачности по громкости: 10%, 50%, 100%.
> **Параметры:** `30` и `15` — пороги.
> **Подкрутить:** Добавь четвёртый уровень. `0, 60, 100` — резче контраст.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
if (amp > 30) 100;
else if (amp > 15) 50;
else 10;
```

### 5.19 Math.random Binary Noise
> **Что делает:** Каждый кадр 0% или 100% случайно — максимальный хаос.
> **Подкрутить:** `* 50` — мигает между 0% и 50%. `seedRandom(index, true)` — фиксирует для каждого слоя.
```javascript
Math.round(random(0, 1)) * 100;
```

### 5.20 Array Index Visibility (Carousel logic)
> **Что делает:** Показывает только слой чей номер = слайдер. Переключатель-карусель.
> **Подкрутить:** `index === activeIndex || index === activeIndex + 1 ? 100 : 0` — два слоя одновременно. Анимируй слайдер для автоматической карусели.
```javascript
const activeIndex = Math.floor(thisComp.layer("CTRL").effect("Slider Control")("Slider"));
index === activeIndex ? 100 : 0;
```

---

## 🎨 6. COLOR & STYLING
> AE colors: 0.0 to 1.0!

### 6.1 Basic Audio RGB Shift
> **Что делает:** Красный канал растёт с амплитудой — краснеет на ударе. G и B фиксированы.
> **Параметры:** `r: 0.2→1.0`. `g=0.5, b=0.5`.
> **Подкрутить:** Поменяй `r` и `g` — зеленеет. Все три в противофазе — цветовой взрыв.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const r = ease(amp, 0, 20, 0.2, 1.0);
const g = 0.5;
const b = 0.5;
[r, g, b, 1];
```

### 6.2 Hue Shift (Color Control)
> **Что делает:** Оттенок сдвигается на удар. Вешай на Color Balance (HLS) → Hue.
> **Параметры:** `0, 180` — сдвиг в градусах.
> **Подкрутить:** `0, 360` — полный круг. `time * 30` добавь — постоянное вращение цвета.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 30, 0, 180);
```

### 6.3 HSL to RGB Converter Function
> **Что делает:** Конвертация HSL → RGB. Управление цветом через понятные параметры.
> **Применение:** `hslToRgb((time*0.5) % 1, 1.0, 0.5)` — радуга за 2 секунды.
> **Подкрутить:** `time*0.1` — медленнее. `0.8` насыщенность — пастельные цвета. `0.7` яркость — светлее.
```javascript
function hslToRgb(h, s, l) {
    let r, g, b;
    if(s == 0) r = g = b = l;
    else {
        const hue2rgb = function(p, q, t){
            if(t < 0) t += 1; if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        };
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }
    return [r, g, b, 1];
}
hslToRgb((time*0.5) % 1, 1.0, 0.5);
```

### 6.4 Audio Brightness / Lightness
> **Что делает:** Яркость растёт на удар. Вешай на Color Balance (HLS) → Lightness.
> **Параметры:** `0, 50`.
> **Подкрутить:** `0, 100` — до белого. `-50, 0` — темнеет. `easeOut` — вспышка с угасанием.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 25, 0, 50);
```

### 6.5 Audio Saturation Burst
> **Что делает:** Насыщенность растёт на удар — в тишине бледно, на ударе сочно. На Hue/Saturation → Master Saturation.
> **Подкрутить:** `ease(amp, 0,25, -50, 100)` — в тишине обесцвеченный.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 25, 0, 100);
```

### 6.6 Interpolate Between Two Colors (Lerp Color)
> **Что делает:** Переход между двумя цветами по амплитуде. Тихо=красный, громко=синий.
> **Подкрутить:** Добавь третий цвет через промежуточный ease. Смени на корпоративные цвета.
```javascript
const c1 = [1, 0, 0, 1];
const c2 = [0, 0, 1, 1];
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const t = ease(amp, 10, 30, 0, 1);
c1 + (c2 - c1) * t;
```

### 6.7 Random Color per Layer
> **Что делает:** Каждый слой — уникальный случайный цвет. Фиксированный.
> **Подкрутить:** `[random(0.5,1), random(0.2,0.5), random(), 1]` — ограниченная гамма. `time` в seed — медленная смена.
```javascript
seedRandom(index, true);
[random(), random(), random(), 1];
```

### 6.8 Pre-defined Color Palette Array
> **Что делает:** Каждый слой выбирает цвет из палитры — все в общей гамме.
> **Подкрутить:** Добавь/убери цвета. `seedRandom(Math.floor(time), true)` — меняется каждую секунду.
```javascript
const palette = [
    [0.9, 0.1, 0.1, 1],
    [0.1, 0.8, 0.3, 1],
    [0.1, 0.4, 0.9, 1],
    [0.9, 0.8, 0.1, 1]
];
seedRandom(index, true);
palette[Math.floor(random(0, palette.length))];
```

### 6.9 Wiggle Color
> **Что делает:** RGB каналы шумят — цвет случайно плавает.
> **Параметры:** `wiggle(2, 0.5)`.
> **Подкрутить:** `wiggle(0.5, 0.3)` — медленная смена. `wiggle(10, 0.1)` — быстрое дрожание.
```javascript
const w = wiggle(2, 0.5);
[clamp(w[0], 0, 1), clamp(w[1], 0, 1), clamp(w[2], 0, 1), 1];
```

### 6.10 Audio Stroke Thickness
> **Что делает:** Толщина обводки растёт с амплитудой. На Stroke → Stroke Width.
> **Параметры:** `2, 25`.
> **Подкрутить:** `10, 2` — тонеет на удар. `easeOut` — резкое утолщение.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 20, 2, 25);
```

### 6.11 Constant Stroke Thickness on Scaled Shape
> **Что делает:** Обводка визуально одинаковой толщины при масштабировании родителя.
> **Подкрутить:** `value / s * 2` — вдвое толще при масштабировании.
```javascript
const s = length(transform.scale) / 100;
value / s;
```

### 6.12 Audio Trim Paths (End)
> **Что делает:** Линия рисует себя на удар — Trim Paths End 0→100%.
> **Подкрутить:** `easeOut` — резко рисуется. `50, 100` — всегда наполовину, достраивается на удар.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 0, 25, 0, 100);
```

### 6.13 Audio Trim Paths (Offset Loop)
> **Что делает:** Пунктир бежит с переменной скоростью — быстрее на ударе.
> **Параметры:** `100, 1000`.
> **Подкрутить:** `1000, 100` — в тишине быстро, на ударе тормозит. `easeOut` — рывок.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const speed = ease(amp, 0, 20, 100, 1000);
time * speed;
```

### 6.14 Glow Intensity via Audio
> **Что делает:** Интенсивность свечения на удар. На Glow → Glow Intensity.
> **Параметры:** `0, 2.5`.
> **Подкрутить:** `0.5, 2` — всегда светится. `0, 5` — яркое.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 10, 30, 0, 2.5);
```

### 6.15 Glow Radius Audio Swell
> **Что делает:** Ореол расширяется на удар. На Glow → Glow Radius.
> **Параметры:** `10, 250`.
> **Подкрутить:** `50, 100` — небольшой диапазон. Комбинируй с 6.14 для полного эффекта.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
ease(amp, 5, 25, 10, 250);
```

### 6.16 Fractal Noise Evolution by Audio
> **Что делает:** Fractal Noise быстрее эволюционирует на ударе. На Fractal Noise → Evolution.
> **Параметры:** `50, 500`.
> **Подкрутить:** `0, 1000` — от стоп-кадра до хаоса. Для жидких текстур.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const speed = ease(amp, 0, 20, 50, 500);
time * speed;
```

### 6.17 Color Phase Shift (Audio)
> **Что делает:** Постоянное медленное изменение фазы + резкий скачок на удар.
> **Подкрутить:** `time * 100` — быстрее. `ease(..., 0, 360)` — полный скачок.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
const basePhase = time * 50;
const kick = ease(amp, 0, 20, 0, 180);
basePhase + kick;
```

### 6.18 Stereo Color Split
> **Что делает:** L → красный, R → синий. Цвет по стерео-балансу.
> **Подкрутить:** Добавь `g` от общей амплитуды. `[r, r*0.3, b, 1]` — теплее/холоднее.
```javascript
const L = thisComp.layer("Audio Amplitude").effect("Left")("Slider");
const R = thisComp.layer("Audio Amplitude").effect("Right")("Slider");
const r = ease(L, 0, 20, 0, 1);
const b = ease(R, 0, 20, 0, 1);
[r, 0, b, 1];
```

### 6.19 Blinking Color Warning
> **Что делает:** На громких ударах мигает красным — аварийная сигнализация.
> **Параметр:** `> 25` — порог.
> **Подкрутить:** `Math.floor(time * 5)` — быстрее мигает.
```javascript
const danger = thisComp.layer("Audio Amplitude").effect("Both")("Slider") > 25;
const red = [1, 0, 0, 1];
const normal = [1, 1, 1, 1];
danger && Math.floor(time * 10) % 2 === 0 ? red : normal;
```

### 6.20 Depth-Based Color Darkening (Fog)
> **Что делает:** Темнеет по мере удаления — атмосферная перспектива.
> **Параметры:** `500, 2000` — дистанция. `1, 0.1`.
> **Подкрутить:** `1, 0.5` — неполное затемнение. Добавь цветной туман через сложение.
```javascript
const cam = thisComp.layer("Camera");
const dist = length(cam.position, position);
const darkFactor = ease(dist, 500, 2000, 1, 0.1);
value * darkFactor;
```

---

## 🔁 7. LOOPS & TIME

### 7.1 Loop Cycle
> **Что делает:** Бесконечно повторяет анимацию после последнего кейфрейма.
> **Подкрутить:** Первый = последний кейфрейм — бесшовно. `loopIn("cycle")` — до первого кейфрейма.
```javascript
loopOut("cycle");
```

### 7.2 Loop Ping Pong
> **Что делает:** Вперёд, потом в обратную сторону — туда-обратно бесконечно.
> **Подкрутить:** Первый и последний НЕ совпадают — нет паузы на краях.
```javascript
loopOut("pingpong");
```

### 7.3 Loop Continue (Momentum)
> **Что делает:** После последнего кейфрейма продолжает с той же скоростью — инерция.
> **Подкрутить:** Хорошо для Rotation — продолжает крутиться. Для Position — ограничь clamp.
```javascript
loopOut("continue");
```

### 7.4 Loop Offset (Accumulation)
> **Что делает:** Каждый цикл добавляет к предыдущему — как лестница. Накапливается.
> **Подкрутить:** Для Position с движением — каждый цикл сдвигается дальше.
```javascript
loopOut("offset");
```

### 7.5 Loop Between Specific Keyframes
> **Что делает:** Зацикливает только последние N кейфреймов — остальная анимация один раз.
> **Параметр:** `2` — количество последних кейфреймов.
> **Подкрутить:** `loopOut("cycle", 3)` — последние три. Для intro + loop фазы.
```javascript
loopOut("cycle", 2);
```

### 7.6 Loop In (Cycle)
> **Что делает:** Loop перед первым кейфреймом.
> **Подкрутить:** `loopIn("pingpong")` — зеркальный. `loopIn("offset")` — накопительный.
```javascript
loopIn("cycle");
```

### 7.7 Time Remap Ping Pong (Audio Synced)
> **Что делает:** Видео перематывается по амплитуде — скрэч-эффект.
> **Подкрутить:** `ease(amp, 0,25, source.duration, 0)` — инверсия. Часть duration — скрэч на участке.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both")("Slider");
ease(amp, 0, 25, 0, source.duration);
```

### 7.8 Posterize Time (Stop Motion)
> **Что делает:** Снижает fps слоя принудительно. СТАВЬ ПЕРВОЙ строкой.
> **Параметр:** `12` — fps.
> **Подкрутить:** `6` — грубый stop motion. `posterizeTime(ease(amp, 0,20, 24, 4))` — choppy на ударах.
```javascript
posterizeTime(12);
value;
```

### 7.9 Math.round Time (1 fps update)
> **Что делает:** Текущая целая секунда — обновляется раз в секунду.
> **Подкрутить:** `Math.floor(time * 2)` — дважды/сек. Для Source Text таймера.
```javascript
Math.floor(time);
```

### 7.10 Frame Counter
> **Что делает:** Текущий номер кадра.
> **Подкрутить:** Source Text — показывает номер. Seed: `seedRandom(timeToFrames(time), true)` — новый рандом/кадр.
```javascript
timeToFrames(time);
```

### 7.11 Time Delay by Layer Index
> **Что делает:** Каждый следующий слой с задержкой 0.1 сек — каскад.
> **Параметр:** `0.1` — шаг.
> **Подкрутить:** `index * 0.3` — медленная волна. Для любого свойства с кейфреймами.
```javascript
valueAtTime(time - (index * 0.1));
```

### 7.12 Time Delay from Comp Center (Radial Wave)
> **Что делает:** Задержка по дистанции от центра — ближние первыми, дальние с опозданием.
> **Параметр:** `dist * 0.001` — 1мс/пиксель.
> **Подкрутить:** `dist * 0.002` — медленнее. Замени `center` — волна из произвольной точки.
```javascript
const center = [thisComp.width/2, thisComp.height/2];
const dist = length(position, center);
const delay = dist * 0.001;
valueAtTime(time - delay);
```

### 7.13 Master Time Slider (Scrub animation)
> **Что делает:** Слайдер управляет временем анимации — перемотка вручную или кейфреймами.
> **Подкрутить:** Анимируй слайдер ease кейфреймами — кастомный timing. Для интерактивных презентаций.
```javascript
const t = thisComp.layer("CTRL").effect("Time Slider")("Slider");
valueAtTime(t);
```

### 7.14 Reverse Animation (Time Remap)
> **Что делает:** Видео задом наперёд.
> **Подкрутить:** `source.duration * 0.5 - time` — реверс с середины.
```javascript
source.duration - time;
```

### 7.15 Loop Animation to Comp Length
> **Что делает:** Зацикливает анимацию каждые `duration` секунд без кейфреймов.
> **Параметр:** `duration = 2`.
> **Подкрутить:** `thisComp.duration` — один проход на весь комп.
```javascript
const duration = 2;
valueAtTime(time % duration);
```

### 7.16 Randomize Start Time (For precomps)
> **Что делает:** Каждый precomp начинает со случайного момента — нет синхронного мигания.
> **Подкрутить:** `random(0, source.duration)` — в пределах footage.
```javascript
seedRandom(index, true);
const offset = random(0, 10);
valueAtTime(time + offset);
```

### 7.17 Stop Animation After Marker
> **Что делает:** Нормально до первого маркера, потом заморозка.
> **Подкрутить:** `marker.key(2).time` — заморозка на втором маркере.
```javascript
if (marker.numKeys > 0) {
    if (time > marker.key(1).time) {
        valueAtTime(marker.key(1).time);
    } else {
        value;
    }
} else {
    value;
}
```

### 7.18 Pulse on Marker Hit
> **Что делает:** На каждый маркер — scale-импульс за 0.5 секунды.
> **Подкрутить:** Расставь маркеры по биту — beat sync без аудио-слоя!
```javascript
let t = 0;
if (marker.numKeys > 0) {
    const m = marker.nearestKey(time);
    t = time - m.time;
    if (t >= 0 && t < 0.5) ease(t, 0, 0.5, 150, 100);
    else 100;
} else 100;
```

### 7.19 Clamp Time to Range
> **Что делает:** Анимация активна только между 2 и 5 секундами.
> **Подкрутить:** `clamp(time, inPoint, outPoint)` — в пределах слоя.
```javascript
valueAtTime(clamp(time, 2, 5));
```

### 7.20 Time-based Spiral
> **Что делает:** Движется по спирали — радиус и угол растут.
> **Параметры:** `time * 50` — расширение. `time * 5` — вращение.
> **Подкрутить:** `time * -50` — сходящаяся спираль.
```javascript
const r = time * 50;
const a = time * 5;
const x = Math.cos(a) * r;
const y = Math.sin(a) * r;
value + [x, y];
```

---

## ⚡ 8. WIGGLE & NOISE

### 8.1 Standard Wiggle
> **Что делает:** Базовый шум Перлина — хаотичное движение без паттерна.
> **Параметры:** `3` — раз/сек. `50` — амплитуда.
> **Подкрутить:** `wiggle(1, 100)` — редкие большие броски. `wiggle(20, 5)` — быстрая мелкая дрожь.
```javascript
wiggle(3, 50);
```

### 8.2 Wiggle on 1 Axis (X)
> **Что делает:** Wiggle только по горизонтали.
> **Подкрутить:** Аудио амплитуда: `wiggle(3, ease(amp, 0,20, 0,80))`.
```javascript
const w = wiggle(3, 50);
[w[0], value[1]];
```

### 8.3 Wiggle on 1 Axis (Y)
> **Что делает:** Wiggle только по вертикали.
> **Подкрутить:** `wiggle(0.5, 200)` — редкие большие вертикальные броски.
```javascript
const w = wiggle(3, 50);
[value[0], w[1]];
```

### 8.4 Audio Reactive Wiggle Amplitude
> **Что делает:** Амплитуда шума от громкости — в тишине стоит, на ударе трясётся.
> **Параметры:** `0, 100` — диапазон wiggle.
> **Подкрутить:** `0, 200` — экстремально. Меняй `5` (частоту) под темп.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both")("Slider");
const wAmt = ease(amp, 0, 25, 0, 100);
wiggle(5, wAmt);
```

### 8.5 Audio Reactive Wiggle Frequency
> **Что делает:** Частота шума от громкости — тихо=медленно, громко=быстрая дрожь.
> **Параметры:** `0.5, 10` — частота.
> **Подкрутить:** `1, 20` — до очень быстрой. Комбинируй с 8.4 — и частота и амплитуда.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both")("Slider");
const wFreq = ease(amp, 0, 25, 0.5, 10);
wiggle(wFreq, 50);
```

### 8.6 Seamless Looping Wiggle
> **Что делает:** Wiggle точно зацикливается — бесшовный loop шума.
> **Параметры:** `loopTime = 4` — длина цикла.
> **Подкрутить:** `loopTime = 2` — короче. `freq = 1` — медленнее. Незаменим для бесконечных фонов.
```javascript
const freq = 2;
const amp = 50;
const loopTime = 4;
const t = time % loopTime;
const w1 = wiggle(freq, amp, 1, 0.5, t);
const w2 = wiggle(freq, amp, 1, 0.5, t - loopTime);
linear(t, 0, loopTime, w1, w2);
```

### 8.7 Posterized (Choppy) Wiggle
> **Что делает:** Сначала замедляет fps до 8, потом шумит — wiggle двигается резкими скачками как stop motion.
> **Параметр:** `8` — fps "скачков". `5, 50` — частота и амплитуда шума.
> **Подкрутить:** `posterizeTime(4)` — грубее, 4 скачка/сек. `posterizeTime(2)` — почти слайдшоу. `wiggle(10, 20)` — мелкие быстрые скачки. Комбинируй с аудио — `posterizeTime(ease(amp,0,20,24,3))` — choppy только на ударах.
```javascript
posterizeTime(8);
wiggle(5, 50);
```

### 8.8 Rounded Sub-Pixel Wiggle
> **Что делает:** Wiggle округляется до целых пикселей — пиксельный стиль движения без дробных координат.
> **Подкрутить:** `Math.round(w[0] / 5) * 5` — шаг 5 пикселей. Хорошо для pixel art анимации и ретро-стилей. Убери `Math.round` с одной оси — одна плавная, другая ступенчатая.
```javascript
const w = wiggle(3, 50);
[Math.round(w[0]), Math.round(w[1])];
```

### 8.9 Noise Function (1D)
> **Что делает:** Одномерный шум Перлина — плавнее и органичнее чем `random()`, но не то же самое что `wiggle()`. Возвращает -1 до 1.
> **Параметр:** `time * 2` — скорость движения через шумовое поле. `* 100` — масштаб выхода.
> **Подкрутить:** `time * 0.5` — медленнее, ленивый дрейф. `time * 10` — быстрый хаос. `noise(time * 2) * 50 + 50` — диапазон 0..100 вместо -100..100.
```javascript
const n = noise(time * 2);
value + (n * 100);
```

### 8.10 Noise Function (2D)
> **Что делает:** Двумерный шум — X и Y независимы через разные смещения seed. Органичнее чем два отдельных wiggle.
> **Параметр:** `100` и `200` — разные seed смещения для X и Y.
> **Подкрутить:** `[time * 2, 0]` и `[time * 2, 999]` — другие смещения. `* 200` — больший диапазон. Замени `100` на `index * 100` — каждый слой своя траектория.
```javascript
const nx = noise([time * 2, 100]);
const ny = noise([time * 2, 200]);
value + [nx * 100, ny * 100];
```

### 8.11 SeedRandom Wiggle (Lock wiggle pattern)
> **Что делает:** Фиксирует паттерн шума через seed — один и тот же wiggle воспроизводится идентично каждый рендер.
> **Параметр:** `12345` — любое число. `false` — паттерн движется со временем (не заморожен).
> **Подкрутить:** `seedRandom(index, false)` — каждый слой свой уникальный паттерн. `seedRandom(42, true)` — полностью заморожено (не двигается). Используй `false` всегда для анимации.
```javascript
seedRandom(12345, false);
wiggle(3, 50);
```

### 8.12 Wiggle Octaves (High detail noise)
> **Что делает:** 5 октав шума — мелкие детали накладываются на крупные. Движение похоже на турбулентность.
> **Параметры:** `wiggle(freq, amp, octaves, mult)`. `5` — октав. `0.5` — каждая следующая октава вдвое тише.
> **Подкрутить:** `octaves = 2` — чуть детальнее обычного. `octaves = 8` — максимально дробное. `mult = 0.7` — октавы убывают медленнее, больше детали.
```javascript
wiggle(2, 100, 5, 0.5);
```

### 8.13 Wiggle Time (Temporal jitter)
> **Что делает:** Вешается на Time Remap — видео случайно скрабирует туда-сюда на ±0.5 секунды. VHS / glitch эффект.
> **Параметр:** `wiggle(2, 0.5)` — 2 раза/сек, ±0.5 сек перемотки.
> **Подкрутить:** `wiggle(5, 0.1)` — быстрое мелкое дрожание кадров. `wiggle(1, 2)` — редкие большие прыжки во времени. Комбинируй с posterizeTime для грубого choppy.
```javascript
const wTime = wiggle(2, 0.5);
wTime;
```

### 8.14 Clamp Wiggle to Positive Only (No going backward)
> **Что делает:** Wiggle движется только в положительную сторону от текущей позиции — не отходит назад.
> **Подкрутить:** `Math.min(value[0], w[0])` — только в отрицательную сторону. `clamp(w[0], value[0]-10, value[0]+100)` — асимметричный диапазон.
```javascript
const w = wiggle(3, 50);
[Math.max(value[0], w[0]), Math.max(value[1], w[1])];
```

### 8.15 Stepped Random Wiggle (Hold keyframe style)
> **Что делает:** Случайное значение меняется каждые `holdTime` секунд и держится — резкие ступенчатые прыжки, не плавный шум.
> **Параметр:** `holdTime = 0.5`. `random(-50, 50)` — диапазон.
> **Подкрутить:** `holdTime = 60/120` — прыжок каждый бит при 120 BPM. `random(0, 360)` — для Rotation. `holdTime = thisComp.frameDuration` — новое значение каждый кадр (максимальный хаос).
```javascript
const holdTime = 0.5;
seedRandom(Math.floor(time / holdTime), true);
random(-50, 50);
```

### 8.16 Wiggle Scale Proportionally
> **Что делает:** Wiggle по Scale с сохранением пропорций — использует только X-компонент шума для обеих осей.
> **Подкрутить:** `wiggle(2, 50)` — медленнее. `wiggle(10, 10)` — быстрая мелкая пульсация. Добавь аудио: `wiggle(5, ease(amp, 0,20, 0,40))`.
```javascript
const w = wiggle(2, 30);
const s = value[0] + (w[0] - value[0]);
[s, s];
```

### 8.17 Wiggle Rotation (Jitter)
> **Что делает:** Добавляет шумовое дрожание к текущему значению Rotation — поверх кейфреймов.
> **Параметры:** `wiggle(10, 15)` — 10 раз/сек, ±15°.
> **Подкрутить:** `wiggle(3, 45)` — медленные большие покачивания. `wiggle(30, 2)` — мелкая быстрая дрожь. `wiggle(5, ease(amp, 0,20, 0,30))` — от аудио.
```javascript
value + wiggle(10, 15);
```

### 8.18 Swarm Wiggle (Offset by index)
> **Что делает:** Каждый слой wiggle-ится по-своему через сдвиг времени на `index * 0.5` — рой, стая, частицы.
> **Параметр:** `index * 0.5` — фазовый сдвиг между слоями. `2, 100` — параметры шума.
> **Подкрутить:** `index * 0.1` — слои почти синхронны. `index * 2` — сильно разбросаны по фазе. `wiggle(0.3, 200, 1, 0.5, time + timeOffset)` — медленный органичный рой.
```javascript
const timeOffset = index * 0.5;
wiggle(2, 100, 1, 0.5, time + timeOffset);
```

### 8.19 Audio Ducking Wiggle (Stops wiggling when loud)
> **Что делает:** Инверсия — трясётся в тишине, успокаивается на ударе. Как испуганный объект который замирает при шуме.
> **Параметры:** `ease(amp, 10, 30, 50, 0)` — амплитуда идёт к нулю при громком.
> **Подкрутить:** `ease(amp, 10, 30, 80, 5)` — не полностью успокаивается. `3` — частота тряски в тишине. Хорошо для атмосферных фоновых элементов.
```javascript
const amp = thisComp.layer("Audio").effect("Both")("Slider");
const wAmt = ease(amp, 10, 30, 50, 0);
wiggle(3, wAmt);
```

### 8.20 Brownian Motion (Random walk)
> **Что делает:** Объект совершает случайное блуждание — каждый кадр смещается на малое случайное расстояние. Имитация диффузии частиц.
> **Параметр:** `random(-2, 2)` — шаг за кадр. `fps` определяет накопление.
> **⚠️ Осторожно:** Цикл до `time * fps` итераций — на длинных компах (>10 сек) будет тормозить. Используй только на коротких сценах или заменяй на `wiggle(0.1, 50)` для похожего результата.
> **Подкрутить:** `random(-5, 5)` — шире шаг. `random(-2, 3)` — смещение в одну сторону (дрейф).
```javascript
const fps = 1.0 / thisComp.frameDuration;
let x = value[0];
let y = value[1];
for (let i = 0; i < time * fps; i++) {
    seedRandom(i, true);
    x += random(-2, 2);
    y += random(-2, 2);
}
[x, y];
```

---

## 🌊 9. PHYSICS & INERTIA
> 20+ physics-based algorithms. Gravity, springs, friction, trailing, momentum — без плагинов.

### 9.1 Classic Inertia Bounce (Overshoot)
> **Что делает:** Добавляет пружинящий overshoot после каждого кейфрейма — объект проскакивает цель и возвращается.
> **Параметры:** `amp = 0.05` — размах отскока. `freq = 2` — частота колебания. `decay = 2` — скорость затухания.
> **Подкрутить:** `amp = 0.1` — сильнее пружинит. `decay = 5` — быстро затухает. `freq = 4` — быстрые колебания. Работает с любым свойством имеющим минимум 2 кейфрейма.
```javascript
const amp = .05;
const freq = 2.0;
const decay = 2.0;
let n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n == 0) value;
else {
    const t = time - key(n).time;
    if (t > 0) {
        const v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
    } else value;
}
```

### 9.2 Spring Physics (Math equation)
> **Что делает:** Анимирует значение от 0 до 100 с пружинным overshoot — без единого кейфрейма, чисто математически.
> **Параметры:** `freq = 3` — жёсткость пружины. `decay = 5` — затухание. `target = 100` — конечное значение.
> **Подкрутить:** `freq = 1, decay = 1` — мягкая медленная пружина. `freq = 8, decay = 3` — жёсткая с несколькими колебаниями. `startVal` и `target` — любые нужные значения свойства.
```javascript
const t = clamp(time - inPoint, 0, 3);
const freq = 3;
const decay = 5;
const target = 100;
const startVal = 0;
startVal + (target - startVal) * (1 - Math.exp(-decay * t) * Math.cos(t * freq * Math.PI * 2));
```

### 9.3 Constant Gravity Fall
> **Что делает:** Объект падает вниз под действием гравитации — ускоряется по параболе.
> **Параметр:** `gravity = 980` — пикселей/сек². Земная гравитация = 9.8 м/с², здесь в пикселях.
> **Подкрутить:** `gravity = 200` — медленное падение (Луна). `gravity = 2000` — тяжёлый объект. Добавь горизонтальную скорость: `value + [200 * t, fallY]` — бросок под углом.
```javascript
const gravity = 980;
const t = time - inPoint;
const fallY = 0.5 * gravity * Math.pow(t, 2);
value + [0, fallY];
```

### 9.4 Friction / Deceleration
> **Что делает:** Объект начинает с большой скоростью и постепенно тормозит до полной остановки — как скольжение по льду.
> **Параметры:** `startSpeed = 1000` — начальная скорость. `friction = 2` — сила трения (выше = быстрее стоп).
> **Подкрутить:** `friction = 0.5` — долгое торможение. `friction = 5` — резкий тормоз. `value + [0, dist]` — по вертикали.
```javascript
const startSpeed = 1000;
const friction = 2;
const t = time - inPoint;
const dist = (startSpeed / friction) * (1 - Math.exp(-friction * t));
value + [dist, 0];
```

### 9.5 Delay Chain (Follow Leader position)
> **Что делает:** Слой повторяет позицию лидера с задержкой пропорциональной разнице индексов. Хвост из объектов.
> **Параметр:** `delay = 0.05` — секунд между каждым слоем.
> **Подкрутить:** `delay = 0.15` — длиннее хвост. Поменяй Leader на Null управляемый мышью — интерактивная змейка.
```javascript
const leader = thisComp.layer("Leader");
const delay = 0.05;
const myIndex = index - leader.index;
leader.position.valueAtTime(time - (myIndex * delay));
```

### 9.6 Delay Chain with Position Offset
> **Что делает:** То же что 9.5, но каждый слой дополнительно смещён по X — хвост растянут в пространстве.
> **Параметр:** `myIndex * 50` — отступ между слоями.
> **Подкрутить:** `[0, myIndex * 50]` — вертикальный хвост. `[myIndex * 30, myIndex * 20]` — диагональный.
```javascript
const leader = thisComp.layer("Leader");
const delay = 0.1;
const myIndex = index - leader.index;
leader.position.valueAtTime(time - (myIndex * delay)) + [myIndex * 50, 0];
```

### 9.7 Rubber Band Follow (Springy connection)
> **Что делает:** Следует за лидером с задержкой + добавляет синусоидальное дрожание — как резинка с вибрацией.
> **Параметры:** `delay = 0.15`, `tension = Math.sin(time * 5) * 20` — амплитуда и частота дрожания.
> **Подкрутить:** `Math.sin(time * 10) * 5` — быстрая мелкая вибрация. `Math.sin(time * 2) * 50` — медленная широкая. `delay = 0.3` — больше инерции.
```javascript
const leader = thisComp.layer("Leader").position;
const delay = 0.15;
const tension = Math.sin(time * 5) * 20;
leader.valueAtTime(time - delay) + [tension, tension];
```

### 9.8 Audio Reactive Bounce (No keyframes)
> **Что делает:** На удар объект подпрыгивает и падает обратно под действием гравитации — без единого кейфрейма.
> **Параметры:** `jump` — высота прыжка от амплитуды. `gravity = 500` — скорость падения. `time % 0.5` — период прыжка.
> **Подкрутить:** `gravity = 200` — медленное падение. `time % 0.25` — быстрые прыжки. `time % 1.0` — медленные долгие прыжки.
```javascript
const amp = thisComp.layer("Audio Amplitude").effect("Both")("Slider");
const jump = linear(amp, 10, 30, 0, 100);
const gravity = 500;
const y = jump > 0 ? jump - (0.5 * gravity * Math.pow(time % 0.5, 2)) : 0;
[value[0], value[1] - Math.max(y, 0)];
```

### 9.9 Soft Inertia Scale (Target tracking)
> **Что делает:** Scale плавно догоняет Scale целевого слоя — инерционное отслеживание.
> **Параметр:** `speed = 0.2` — насколько быстро догоняет (0.01 = медленно, 0.5 = быстро).
> **Подкрутить:** `speed = 0.05` — ленивое следование с длинным хвостом. `speed = 0.4` — почти мгновенно. ⚠️ Нужен стартовый кейфрейм.
```javascript
const target = thisComp.layer("Target").scale[0];
const current = value[0];
const speed = 0.2;
const s = current + (target - current) * speed;
[s, s];
```

### 9.10 Dampened Oscillator (Like a guitar string)
> **Что делает:** Объект колышется как струна — максимальная амплитуда в `hitTime`, затем затухает.
> **Параметры:** `hitTime = 1.0` — момент "удара". `freq = 5` — частота. `decay = 2` — затухание. `amp = 50` — начальная амплитуда.
> **Подкрутить:** `freq = 2` — низкая нота, медленные колебания. `freq = 15` — высокая нота. `decay = 0.5` — долго звучит. Вешай на Position, Scale или Rotation.
```javascript
const hitTime = 1.0;
const t = Math.max(0, time - hitTime);
const amp = 50;
const freq = 5;
const decay = 2;
value + Math.exp(-decay * t) * Math.cos(freq * t * Math.PI * 2) * amp;
```

### 9.11 Orbit with Decaying Radius
> **Что делает:** Орбита постепенно сужается — объект по спирали движется к центру как спутник входящий в атмосферу.
> **Параметры:** `initialRadius = 500` — начальный радиус. `decay = 0.5` — скорость сужения. `angle = t * 5` — скорость вращения.
> **Подкрутить:** `decay = 0.1` — медленно сужается. `decay = 2` — быстро падает к центру. `t * 10` — быстрее крутится. Инверсия: `* Math.exp(+decay * t)` — расширяющаяся спираль.
```javascript
const t = time;
const initialRadius = 500;
const decay = 0.5;
const radius = initialRadius * Math.exp(-decay * t);
const angle = t * 5;
[value[0] + Math.cos(angle) * radius, value[1] + Math.sin(angle) * radius];
```

### 9.12 Velocity-Based Scale (Squash and Stretch)
> **Что делает:** Автоматический squash-stretch по скорости — быстро движется = вытягивается. Физически правдоподобно.
> **Параметр:** `speed / 1000` — коэффициент растяжения. `1 / stretch` — squash обратно пропорционален.
> **Подкрутить:** `speed / 500` — сильнее деформируется. `speed / 2000` — едва заметно. Ограничь через `clamp` чтобы не деформировалось слишком сильно.
```javascript
const v = position.velocity;
const speed = length(v);
const stretch = 1 + (speed / 1000);
const squash = 1 / stretch;
[value[0] * stretch, value[1] * squash];
```

### 9.13 Auto-Banking on Turns (Velocity direction)
> **Что делает:** Самолёт кренится в повороты — крен пропорционален горизонтальной скорости.
> **Параметр:** `0.05` — коэффициент крена (выше = сильнее кренится).
> **Подкрутить:** `0.1` — сильный крен. `v[1] * 0.05` — крен от вертикальной скорости. `clamp(value + roll, -45, 45)` — ограничь максимальный крен.
```javascript
const v = position.velocity;
const roll = v[0] * 0.05;
value + roll;
```

### 9.14 Hover / Floating Physics
> **Что делает:** Парение с уникальной фазой для каждого слоя — объекты в группе парят вразнобой.
> **Параметры:** `freq = 1`, `amp = 15`, `phase = index * 10` — фазовый сдвиг.
> **Подкрутить:** `index * 30` — сильнее разброс фаз. `amp = 40` — выше парит. `freq = 0.5` — медленнее. Хорошо для иконок, карточек, частиц.
```javascript
const freq = 1;
const amp = 15;
const phase = index * 10;
const y = Math.sin(time * freq * Math.PI * 2 + phase) * amp;
value + [0, y];
```

### 9.15 Follow Null Rotation
> **Что делает:** Копирует Rotation нулла с задержкой — ленивое следование за поворотом.
> **Параметр:** `delay = 0.1` — секунд задержки.
> **Подкрутить:** `delay = 0.5` — длинная задержка. Цепочка: каждый следующий слой читает предыдущий — волна вращений.
```javascript
const leader = thisComp.layer("Null").rotation;
const delay = 0.1;
leader.valueAtTime(time - delay);
```

### 9.16 Fake Wind (Wiggle with bias)
> **Что делает:** Wiggle + постоянный дрейф вправо — имитация ветра: объект хаотично дрейфует но в целом летит вправо.
> **Параметр:** `100 * time` — скорость ветра в пикселях/сек.
> **Подкрутить:** `50 * time` — слабый ветер. `[0, -80 * time]` — ветер снизу вверх (дым, пар). `[-100 * time, 0]` — ветер слева.
```javascript
const w = wiggle(2, 50);
const windBias = [100 * time, 0];
[w[0] + windBias[0], w[1]];
```

### 9.17 Repel Force (Magnetism)
> **Что делает:** Объект отталкивается от "Cursor" обратно пропорционально расстоянию — ближе = сильнее толкает.
> **Параметры:** `force = 10000` — сила. `maxDist = 200` — радиус действия.
> **Подкрутить:** `force = 50000` — очень сильное отталкивание. `maxDist = 400` — широкая зона. Замени `value - cursor` на `cursor - value` — притягивает (гравитационный колодец).
```javascript
const cursor = thisComp.layer("Cursor").position;
const dist = length(cursor, value);
const force = 10000;
const maxDist = 200;
if (dist < maxDist && dist > 0) {
    const dir = normalize(value - cursor);
    value + dir * (force / dist);
} else {
    value;
}
```

### 9.18 Attract Force (Gravity Well)
> **Что делает:** Объект притягивается к "BlackHole" — чем ближе, тем сильнее. В пределах 500px.
> **Параметр:** `strength = 0.1` — сила притяжения за кадр.
> **Подкрутить:** `strength = 0.3` — быстро затягивает. `dist < 200` — меньший радиус. Комбинируй с 9.16 — ветер тянет в одну сторону, колодец притягивает в центр.
```javascript
const hole = thisComp.layer("BlackHole").position;
const dist = length(hole, value);
const strength = 0.1;
if (dist < 500) {
    value + (hole - value) * strength;
} else {
    value;
}
```

### 9.19 Jello Wobble (Frequency driven by speed)
> **Что делает:** Scale вибрирует — быстрее движется объект, сильнее "желеобразная" тряска.
> **Параметр:** `speed * 0.05` — коэффициент вибрации. `time * 15` — частота желе.
> **Подкрутить:** `time * 8` — медленнее, видны волны. `time * 30` — быстрая дрожь. `speed * 0.1` — сильнее реагирует на скорость.
```javascript
const speed = length(position.velocity);
const wobbleAmp = speed * 0.05;
const s = value[0] + Math.sin(time * 15) * wobbleAmp;
[s, s];
```

### 9.20 Momentum Scroll (Infinite list)
> **Что делает:** Бесконечный вертикальный скролл — контент прокручивается и зацикливается через modulo.
> **Параметры:** `speed = 500` — пикселей/сек. `height = 1000` — высота контента (полный цикл).
> **Подкрутить:** `speed = 200` — медленнее. `speed = ease(amp, 0,20, 200, 1000)` — ускоряется под бит. По X: `[value[0] - (time * speed) % width, value[1]]` — горизонтальный скролл.
```javascript
const speed = 500;
const height = 1000;
const y = (time * speed) % height;
[value[0], value[1] - y];
```

---

## 🔗 10. LAYER SPACE & RIGGING
> 20+ systems for rigging UIs, connecting properties, parenting offsets, and complex data logic.

### 10.1 Slider Control Array Selector
> **Что делает:** Слайдер выбирает значение из массива — вместо кейфреймов нужного числа просто ставишь целое значение слайдера.
> **Параметр:** `vals = [10, 50, 120, 300]` — набор значений. Слайдер 0=10, 1=50, 2=120, 3=300.
> **Подкрутить:** Добавь больше значений. Слайдер `1.5` → округляется до `1` = 50. Используй для выбора цветов из палитры, размеров, состояний.
```javascript
const vals = [10, 50, 120, 300];
const s = Math.floor(thisComp.layer("CTRL").effect("Slider")("Slider"));
vals[clamp(s, 0, vals.length - 1)];
```

### 10.2 toComp() — True World Position
> **Что делает:** Находит абсолютные экранные координаты слоя с любым количеством пэрентов. Игнорирует всю иерархию трансформаций.
> **Подкрутить:** Передай результат в `fromComp()` другого слоя — телепортируй объект в экранную позицию другого. Используй для выравнивания слоёв из разных групп.
```javascript
const target = thisComp.layer("Null 1");
target.toComp(target.anchorPoint);
```

### 10.3 fromComp() — Convert World to Local
> **Что делает:** Конвертирует мировую точку в локальные координаты текущего слоя — учитывает все пэрент-трансформации.
> **Подкрутить:** `fromComp(thisComp.layer("A").toComp([0,0]))` — снэп к позиции другого слоя в локальном пространстве. Незаменим в сложных иерархиях.
```javascript
const worldPoint = thisComp.layer("Target").position;
fromComp(worldPoint);
```

### 10.4 Auto-Orient (LookAt Target 2D)
> **Что делает:** Вычисляет угол поворота к целевому слою — объект всегда смотрит на Target.
> **Подкрутить:** `+ 90` — перпендикулярно к цели (боком). `+ 180` — лицом от цели. Замени `"Target"` на Null под мышью — интерактивный прицел.
```javascript
const target = thisComp.layer("Target").position;
const delta = target - position;
radiansToDegrees(Math.atan2(delta[1], delta[0]));
```

### 10.5 Maintain Visual Scale when Parent Scales
> **Что делает:** Дочерний слой остаётся визуально одного размера когда родитель масштабируется — компенсирует Scale.
> **Подкрутить:** `* 0.5` после деления — дочерний полувидимо масштабируется. Хорошо для текстов и UI элементов на масштабируемых контейнерах.
```javascript
const p = parent;
if (p) {
    const sX = (value[0] / p.transform.scale[0]) * 100;
    const sY = (value[1] / p.transform.scale[1]) * 100;
    [sX, sY];
} else value;
```

### 10.6 Maintain Rotation when Parent Rotates
> **Что делает:** Дочерний слой остаётся горизонтальным когда родитель вращается — компенсирует Rotation.
> **Подкрутить:** `value - parent.transform.rotation * 0.5` — полукомпенсация, частично следует. Для текста на вращающихся объектах, кабинок колеса обозрения.
```javascript
parent ? value - parent.transform.rotation : value;
```

### 10.7 Checkbox Toggle Switch
> **Что делает:** Чекбокс на CTRL включает/выключает значение — простой переключатель.
> **Подкрутить:** `cb == 1 ? 100 : 30` — выключенный не 0 а 30%. Несколько чекбоксов — несколько независимых переключателей.
```javascript
const cb = thisComp.layer("CTRL").effect("Checkbox Control")("Checkbox");
cb == 1 ? 100 : 0;
```

### 10.8 Dropdown Menu Control (AE 2020+)
> **Что делает:** Dropdown на CTRL выбирает из набора значений — меню состояний объекта.
> **Параметры:** `menu == 1`, `2`, `3` — пункты меню начиная с 1.
> **Подкрутить:** Добавь `else if (menu == 3)` для третьего состояния. Используй для переключения между разными Scale/Position/Opacity конфигурациями.
```javascript
const menu = thisComp.layer("CTRL").effect("Dropdown Menu Control")("Menu");
if (menu == 1) [100, 100];
else if (menu == 2) [200, 200];
else [50, 50];
```

### 10.9 Clamp Layer to Composition Bounds
> **Что делает:** Объект не выходит за края компа — автоматические границы по размеру компа.
> **Подкрутить:** `clamp(value[0], 100, thisComp.width - 100)` — с отступом 100px. Используй вместе с физикой (9.3, 9.4) — объект падает и отскакивает от края.
```javascript
const x = clamp(value[0], 0, thisComp.width);
const y = clamp(value[1], 0, thisComp.height);
[x, y];
```

### 10.10 Text Source Link
> **Что делает:** Source Text отображает текущее значение Slider в процентах — живой числовой дисплей.
> **Подкрутить:** `Math.round(s) + " px"` — в пикселях. `Math.round(s * 10) / 10 + ""` — с одним знаком после запятой. `"Volume: " + Math.round(s) + "%"` — с лейблом.
```javascript
const s = thisComp.layer("CTRL").effect("Slider")("Slider");
Math.round(s) + "%";
```

### 10.11 Dynamic Anchor Point (Center of Text)
> **Что делает:** Автоматически ставит Anchor Point в визуальный центр текстового слоя — независимо от содержимого.
> **Подкрутить:** `[box.left, box.top + box.height/2]` — якорь по левому краю в центре высоты. Незаменим для текстов разной длины чтобы Scale всегда шёл от центра.
```javascript
const box = sourceRectAtTime();
[box.left + box.width/2, box.top + box.height/2];
```

### 10.12 Dynamic Background Box (Auto-sizing)
> **Что делает:** Shape Layer автоматически подстраивает размер под текст + padding. Фон текста живой.
> **Параметр:** `pad = 50` — отступ с каждой стороны.
> **Подкрутить:** `pad = 20` — меньший отступ. `[box.width + pad, box.height * 2]` — фиксированная высота. Поменяй `"Text"` на имя своего текстового слоя.
```javascript
const t = thisComp.layer("Text");
const pad = 50;
const box = t.sourceRectAtTime();
[box.width + pad, box.height + pad];
```

### 10.13 Master Color Controller
> **Что делает:** Читает цвет из Color Control на CTRL — меняешь один раз, обновляется везде.
> **Подкрутить:** Добавь второй Color Control `"Accent Color"` для вторичного цвета. Умножь результат на `ease(amp, 0,20, 0.5, 1)` — цвет ярче на ударе.
```javascript
thisComp.layer("CTRL").effect("Theme Color")("Color");
```

### 10.14 Opacity by Distance (Measuring tape)
> **Что делает:** Opacity зависит от расстояния между двумя Null-слоями — дальше друг от друга = прозрачнее.
> **Параметры:** `100, 500` — диапазон дистанции.
> **Подкрутить:** `ease(dist, 0, 200, 100, 0)` — исчезает когда близко. Используй для визуализации "зоны действия" или дистанции между объектами.
```javascript
const p1 = thisComp.layer("Point A").position;
const p2 = thisComp.layer("Point B").position;
const dist = length(p1, p2);
ease(dist, 100, 500, 100, 0);
```

### 10.15 Line Draw Between Two Nulls (Beam effect)
> **Что делает:** Получает мировые координаты Null A для привязки начальной точки эффекта Beam.
> **Применение:** На Effect → Generate → Beam → Starting Point вешай этот expression, на Ending Point — аналогично для Null B.
> **Подкрутить:** `toComp([0,0])` — точка в центре Null. `toComp([50, 0])` — смещение от центра.
```javascript
thisComp.layer("Null A").toComp([0,0]);
```

### 10.16 Percentage Loader String
> **Что делает:** Анимированный счётчик процентов от 0% до 100% за 2 секунды от inPoint.
> **Параметр:** `inPoint + 2` — 2 секунды на загрузку.
> **Подкрутить:** `inPoint + 5` — медленнее. `Math.floor(loaded)` → `Math.ceil(loaded)` — округление вверх. `"Loading " + ... + "% complete"` — другой формат строки.
```javascript
const loaded = ease(time, inPoint, inPoint + 2, 0, 100);
Math.floor(loaded) + "%";
```

### 10.17 Parent to Point on Shape (Path Data)
> **Что делает:** Возвращает координаты конкретной вершины пути шейп-слоя. Привязка к точке формы.
> **Параметр:** `pointIndex = 0` — номер вершины (0 = первая).
> **Подкрутить:** `pointIndex = 2` — третья вершина. `path.points()[1]` — вторая точка. Используй для привязки объектов к углам звезды, полигона и т.д.
```javascript
const path = thisComp.layer("Shape").content("Path 1").path;
const pointIndex = 0;
path.points()[pointIndex];
```

### 10.18 Trace Path Progress
> **Что делает:** Объект движется вдоль пути шейп-слоя — проходит весь контур за 2 секунды, зациклено.
> **Параметр:** `time % 2` — длина одного обхода пути.
> **Подкрутить:** `time % 4` — медленнее. `ease(time % 2, 0, 2, 0, 1)` — плавное ускорение/торможение по пути. `(time % 2) / 2 * 0.5` — только половина пути.
```javascript
const path = thisComp.layer("Shape").content("Path 1").path;
const progress = (time % 2) / 2;
path.pointOnPath(progress);
```

### 10.19 Angle on Path
> **Что делает:** Вычисляет угол касательной к пути в текущей точке — объект автоматически ориентируется по направлению движения вдоль пути.
> **Подкрутить:** `+ 90` — перпендикулярно пути. Комбинируй с 10.18 на Position — объект едет по пути и смотрит вперёд.
```javascript
const path = thisComp.layer("Shape").content("Path 1").path;
const progress = (time % 2) / 2;
const vec = path.tangentOnPath(progress);
radiansToDegrees(Math.atan2(vec[1], vec[0]));
```

### 10.20 Master Audio Gate (Rig Toggle)
> **Что делает:** Глобальный включатель beat sync — чекбокс "Enable Beat Sync" на CTRL включает/выключает всю аудио-реакцию рига не ломая expressions.
> **Подкрутить:** `switchOn == 1 ? ease(amp, ...) : value` — в выключенном состоянии возвращает кейфреймовое значение. Добавь второй чекбокс для процедурного движения — полный контроль над ригом из одного места.
```javascript
const amp = thisComp.layer("Audio").effect("Both")("Slider");
const switchOn = thisComp.layer("CTRL").effect("Enable Beat Sync")("Checkbox");
switchOn == 1 ? linear(amp, 0, 20, 100, 150) : 100;
```

---

> **🎛️ Annotated V3 Edition.**
> Каждый expression объяснён: что делает, какой параметр за что отвечает, что подкрутить.
> Анимируй всё. Бойся ничего. Пусть код делает тяжёлую работу.

