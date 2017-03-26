from PIL import Image
import sys


def ocr(im, threshold=100, mask="tr-2.png", alphabet="7hnNW6xH"):
    img = Image.open(im)
    img = img.convert("RGB")
    # box = (8, 8, 58, 18)
    # img = img.crop(box)
    # box = img.getbbox()
    pixdata = img.load()

    # open the mask
    letters = Image.open(mask)
    ledata = letters.load()

    def test_letter(img, letter):
        A = img.load()
        B = letter.load()
        mx = 1000000
        max_x = 0
        x = 0
        for x in range(img.size[0] - letter.size[0]):
            _sum = 0
            for i in range(letter.size[0]):
                for j in range(letter.size[1]):
                    _sum = _sum + abs(A[x + i, j][0] - B[i, j][0])
            if _sum < mx:
                mx = _sum
                max_x = x
        return mx, max_x

    # Clean the background noise, if color != white, then set to black.
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] > threshold) \
                    and (pixdata[x, y][1] > threshold) \
                    and (pixdata[x, y][2] > threshold):

                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)

    counter = 0
    old_x = -1

    letterlist = []

    black_pre = True
    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y][0] != 0:
                if black_pre:
                    old_x = x
                black = False
                black_pre = False
                break
        if black:
            if black_pre:
                old_x = x
                continue
            black_pre = True
            box = (old_x + 1, 0, x, letters.size[1])
            print 'save letter %d to %d' % (old_x, x)
            letter = letters.crop(box)
            letter.save('letter-img-%d_%d.png'%(old_x,x))
            t = test_letter(img, letter)
            letterlist.append((t[0], alphabet[counter], t[1]))
            print letterlist
            counter += 1
            black_pre = True
            print 'save letter done'

    t = sorted(letterlist)
    t = t[0:4]  # 4-letter captcha

    final = sorted(t, key=lambda e: e[2])

    answer = ''.join(map(lambda l: l[1], final))
    # answer = ""
    # for l in final:
    #     answer = answer + l[1]
    return answer


if __name__ == '__main__':
    print(ocr(sys.argv[1]))
