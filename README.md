# Growtopia Captcha Solver

# Parse Captcha UID

Varlist

```txt
param 0: onShowCaptcha
param 1: add_puzzle_captcha|0098/captcha/generated/2515b3da-7868-408a-818c-c2ba12ca2287-PuzzleWithMissingPiece.rttex|0098/captcha/generated/2515b3da-7868-408a-818c-c2ba12ca2287-TrimmedPuzzlePiece.rttex|ubistatic-a.akamaihd.net|200118|
end_dialog|puzzle_captcha_submit||Submit|
2515b3da-7868-408a-818c-c2ba12ca2287-PuzzleWithMissingPiece.rttex -> Captcha UID = 2515b3da-7868-408a-818c-c2ba12ca2287
Captcha UID = 2515b3da-7868-408a-818c-c2ba12ca2287
```

# API
```http://52.140.200.84:5000/captcha=[CaptchaUID]```

# Example
Request Method = GET

```curl http://52.140.200.84:5000/captcha=2515b3da-7868-408a-818c-c2ba12ca2287```

http://52.140.200.84:5000/captcha=2515b3da-7868-408a-818c-c2ba12ca2287

# Response
Solved :
```txt
0.48046875
```
Failed :
```txt
- Failed
- Invalid Captcha UID
```
