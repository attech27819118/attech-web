for p in ['about/index.html', 'contact/index.html', 'partners/index.html', 'products/index.html', 'products/dorfketal/chain/ClearLink 1000/index.html']:
    with open(p, encoding='utf-8') as f:
        c = f.read()
    print(f"=== {p} ===")
    print("  nav-technology:", "nav-technology" in c)
    print("  mobile-nav-technology:", "mobile-nav-technology" in c)
    print("  contact-success-state:", "contact-success-state" in c)
    print("  technology.js:", "technology.js" in c)

