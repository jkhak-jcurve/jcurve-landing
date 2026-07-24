#!/usr/bin/env python3
"""Vercel 이전 시 OG 절대주소 도메인 일괄 치환 스크립트.

og:url / og:image 등이 GitHub Pages 절대주소로 박혀 있어,
도메인 전환 시 이 스크립트로 새 도메인으로 치환한다.

사용법 (저장소 루트에서):
    python3 tools/migrate-domain.py                          # 드라이런(변경 대상만 출력)
    python3 tools/migrate-domain.py --apply                  # 기본 새 도메인으로 치환
    python3 tools/migrate-domain.py --apply --to https://jcurveschool.com/

치환 후 확인:
    grep -rl "jkhak-jcurve.github.io" *.html cases/*.html   # 0건이어야 함
"""
import argparse, glob, sys

OLD_BASE = "https://jkhak-jcurve.github.io/jcurve-landing/"
NEW_BASE_DEFAULT = "https://jcurveschool.com/"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 치환 (없으면 드라이런)")
    ap.add_argument("--to", default=NEW_BASE_DEFAULT, help="새 도메인 베이스 URL (끝에 / 포함)")
    args = ap.parse_args()
    if not args.to.endswith("/"):
        sys.exit("오류: --to 값은 /로 끝나야 합니다: " + args.to)

    files = sorted(glob.glob("*.html") + glob.glob("cases/*.html"))
    if not files:
        sys.exit("오류: HTML 파일이 없습니다. 저장소 루트에서 실행하세요.")

    total = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        n = src.count(OLD_BASE)
        if not n:
            continue
        total += n
        print(f"{'치환' if args.apply else '대상'}: {f} ({n}곳)")
        if args.apply:
            open(f, "w", encoding="utf-8").write(src.replace(OLD_BASE, args.to))

    mode = "치환 완료" if args.apply else "드라이런 (적용하려면 --apply)"
    print(f"\n{mode}: 총 {total}곳 / 새 도메인: {args.to}")

if __name__ == "__main__":
    main()
