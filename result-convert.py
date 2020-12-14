with open("1-10t-results.txt", "r+") as f:
    text = f.readlines()

text = [line.strip() for line in text]

res = "\n".join(", ".join(two_lines) for two_lines in zip(text[::2], text[1::2])) + (
    text[-1] if len(text) % 2 != 0 else '')

print(res)
with open("result.csv", "w+") as f:
    f.writelines(["model, formula, threads, wall, user, sys, peak mem\n"])
    f.writelines(res)
