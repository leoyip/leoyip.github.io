---
title: Swift学习笔记
date: 2015-01-06 12:00:00
categories: 技术
tags:
  - Swift
  - iOS
---

## 1、值永远不会被隐式转换为其他类型

如果你需要把一个值转换成其他类型，请显式转换。

```swift
let label = "The width is"
let width = 94
let widthLabel = label + String(width)
```

删除最后一行中的 `String`，错误提示：`Could not find an overload for '+' that accepts the supplied arguments`

## 2、switch 支持任意类型的数据

switch 支持任意类型的数据以及各种比较操作——不仅仅是整数以及测试相等。

```swift
let vegetable = "red pepper"
switch vegetable {
case "celery":
    let vegetableComment = "Add some raisins and make ants on a log."
case "cucumber", "watercress":
    let vegetableComment = "That would make a good tea sandwich."
case let x where x.hasSuffix("pepper"):
    let vegetableComment = "Is it a spicy \(x)?"
default:
    let vegetableComment = "Everything tastes good in soup."
}
```

删除 default 语句，报错：`Switch must be exhaustive, consider adding a default clause`

运行 switch 中匹配到的子句之后，程序会退出 switch 语句，并不会继续向下运行，所以不需要在每个子句结尾写 break。

## 3、常量和变量的命名

你可以用任何你喜欢的字符作为常量和变量名，包括 Unicode 字符：

```swift
let π = 3.14159
let 你好 = "你好世界"
let 🐶🐮 = "dogcow"
```

常量与变量名不能包含数学符号，箭头，保留的（或者非法的）Unicode 码位，连线与制表符。也不能以数字开头，但是可以在常量与变量名的其他地方包含数字。

## 4、输出常量和变量

你可以用 `println` 函数来输出当前常量或变量的值：

```swift
println(friendlyWelcome)
// 输出 "Bonjour!"
```

`println` 是一个用来输出的全局函数，输出的内容会在最后换行。如果你用 Xcode，println 将会输出内容到"console"面板上。(另一种函数叫 `print`，唯一区别是在输出内容最后不会换行。)

## 5、数值型字面量

整数字面量可以被写作：

- 一个十进制数，没有前缀
- 一个二进制数，前缀是 `0b`
- 一个八进制数，前缀是 `0o`
- 一个十六进制数，前缀是 `0x`

下面的所有整数字面量的十进制值都是17：

```swift
let decimalInteger = 17
let binaryInteger = 0b10001       // 二进制的17
let octalInteger = 0o21           // 八进制的17
let hexadecimalInteger = 0x11     // 十六进制的17
```

浮点字面量可以是十进制（没有前缀）或者是十六进制（前缀是0x）。小数点两边必须有至少一个十进制数字（或者是十六进制的数字）。

- `1.25e2` 表示 $1.25 \times 10^{2}$，等于 125.0
- `1.25e-2` 表示 $1.25 \times 10^{-2}$，等于 0.0125
- `0xFp2` 表示 $15 \times 2^{2}$，等于 60.0
- `0xFp-2` 表示 $15 \times 2^{-2}$，等于 3.75

## 6、可选（Optionals）

使用可选（optionals）来处理值可能缺失的情况。可选表示：**有值，等于 x** 或者 **没有值**。

注意：C 和 Objective-C 中并没有可选这个概念。

来看一个例子：

```swift
let possibleNumber = "123"
let convertedNumber = possibleNumber.toInt()
// convertedNumber 被推测为类型 "Int?"，或者类型 "optional Int"
```

因为 `toInt` 方法可能会失败，所以它返回一个可选的（optional）Int，而不是一个 Int。一个可选的 Int 被写作 `Int?` 而不是 `Int`。

## 7、多个 case 匹配同一个值

不像C语言，Swift 允许多个 case 匹配同一个值。但是，如果存在多个匹配，那么只会执行第一个被匹配到的 case 块。
