# Beachy Barns Staging Site - QA Report & Checklist

**Staging URL:** https://beachybarnstaging.dreamhosters.com
**Production URL:** https://www.beachybarns.com
**Prepared for:** Web Design Team
**Date:** 2026-02-06

---

## How to Use This Report

This report maps **every known page** on the Beachy Barns website. For each page:
1. Visit the staging URL listed
2. Check each bullet point issue/item
3. Mark items as PASS / FAIL / N/A
4. Add notes for anything that needs fixing

**To run the automated crawler** (finds broken links, 404s, missing images automatically):
```bash
pip install requests beautifulsoup4 lxml
python src/staging_qa_report.py https://beachybarnstaging.dreamhosters.com/ \
  --wp-user "Jonathan Dominise" --wp-pass "JDominise321!" \
  --max-pages 300 -o automated_qa_report.md --json qa_report.json
```

---

## Site Map Overview (All Known Pages)

### Main Pages
| # | Page | Staging URL |
|---|------|-------------|
| 1 | Homepage | /  |
| 2 | Storage Sheds (parent) | /storage-sheds/ |
| 3 | Shed Sizes (parent) | /shed-sizes/ |
| 4 | Garages | /garages/ |
| 5 | Inventory | /inventory/ |
| 6 | Rent-to-Own | /rent-to-own/ |
| 7 | On-Site Build | /on-site-build/ |
| 8 | Shed Options | /shed-options/ |
| 9 | Download Catalog | /download-a-catalog/ |
| 10 | Site Preparation | /site-preparation/ |
| 11 | Tips & Stories (Blog) | /tips-stories/ |
| 12 | Contact / Free Quote | /contact/ or /free-quote/ |
| 13 | About | /about/ |

### Shed Style Pages
| # | Page | Staging URL |
|---|------|-------------|
| 14 | Gable Sheds | /storage-sheds/gable-sheds/ |
| 15 | Quaker Sheds | /storage-sheds/quaker/ |
| 16 | Cape Cod Sheds | /storage-sheds/cape-cod-sheds/ |
| 17 | Classic Sheds | /storage-sheds/classic/ |
| 18 | Mini Barn | /storage-sheds/mini-barn/ |
| 19 | Cottage Sheds | /storage-sheds/cottage/ |
| 20 | Cabin Sheds | /storage-sheds/cabin/ |
| 21 | Retreat (Sheds w/ Porches) | /storage-sheds/retreat/ |
| 22 | Highwall Sheds | /storage-sheds/highwall/ |
| 23 | Premier Highwall | /storage-sheds/premier-highwall/ |
| 24 | Modern Studio | /storage-sheds/modern-studio/ |
| 25 | Shed Bar | /storage-sheds/shed-bar/ |
| 26 | Custom Sheds | /storage-sheds/custom/ |

### Garage Pages
| # | Page | Staging URL |
|---|------|-------------|
| 27 | Highwall Garage | /garages/highwall-garage-shed/ |
| 28 | Gable Garage | /garages/gable-garage/ |

### Shed Size Pages
| # | Page | Staging URL |
|---|------|-------------|
| 29 | 6x6 Sheds | /shed-sizes/6x6-sheds/ |
| 30 | 6x8 Sheds | /shed-sizes/6x8-sheds/ |
| 31 | 8x10 Sheds | /shed-sizes/8x10-sheds/ |
| 32 | 8x12 Sheds | /shed-sizes/8x12-sheds/ |
| 33 | 10x10 Sheds | /shed-sizes/10x10-sheds/ |
| 34 | 10x12 Sheds | /shed-sizes/10x12-sheds-in-ohio/ |
| 35 | 10x14 Sheds | /shed-sizes/10x14-sheds/ |
| 36 | 10x16 Sheds | /shed-sizes/10x16-sheds/ |
| 37 | 12x16 Sheds | /shed-sizes/12x16-sheds/ |
| 38 | 12x20 Sheds | /shed-sizes/12x20-sheds/ |
| 39 | 12x24 Sheds | /shed-sizes/12x24-sheds/ |
| 40 | 14x20 Sheds | /shed-sizes/14x20-sheds/ |
| 41 | 14x24 Sheds | /shed-sizes/14x24-sheds/ |
| 42 | 16x28 Sheds | /shed-sizes/16x28-sheds/ |

### Location Pages
| # | Page | Staging URL |
|---|------|-------------|
| 43 | Columbus | /locations/sheds-in-columbus-ohio/ |
| 44 | Dayton | /locations/sheds-in-dayton-ohio/ |
| 45 | Fairborn | /locations/storage-sheds-in-fairborn-ohio/ |
| 46 | Springfield | /locations/sheds-in-springfield-ohio/ |
| 47 | Cincinnati | /locations/storage-buildings-in-cincinnati-ohio/ |
| 48 | Dublin | /locations/sheds-in-dublin-ohio/ |
| 49 | Kettering | /locations/storage-buildings-in-kettering-ohio/ |
| 50 | Huber Heights | /locations/backyard-sheds-in-huber-heights-ohio/ |
| 51 | Beaver Creek | /locations/storage-buildings-in-beaver-creek-ohio/ |
| 52 | Lancaster | /locations/storage-buildings-in-lancaster-ohio/ |
| 53 | Newark | /locations/storage-buildings-in-newark-ohio/ |
| 54 | Westerville | /locations/sheds-for-sale-westerville-ohio/ |
| 55 | Worthington | /locations/sheds-for-sale-in-worthington-oh/ |
| 56 | Grove City | /locations/sheds-for-sale-in-grove-city-oh/ |
| 57 | Blacklick Estates | /locations/sheds-for-sale-in-blacklick-estates-ohio/ |
| 58 | Delaware | /locations/storage-buildings-delaware/ |
| 59 | Indian Lake | /locations/sheds-in-indian-lake-ohio/ |
| 60 | Marysville | /locations/prefab-buildings-in-marysville-ohio/ |

### Blog / Tips & Stories Pages
| # | Page | Staging URL |
|---|------|-------------|
| 61 | Tips & Stories Index | /tips-stories/ |
| 62 | The Home Farm | /tips-stories/the-home-farm/ |
| 63 | Deciding What Size Shed | /tips-stories/deciding-what-size-shed-you-need/ |
| 64 | 8x10 Shed Pros & Cons | /tips-stories/8-x-10-storage-shed-pros-and-cons/ |
| 65 | 10x10 Sheds Everything to Know | /10x10-sheds-everything-you-need-to-know/ |
| 66 | 10x12 Sheds | /tips-stories/10x12-sheds/ |
| 67 | Vinyl Siding for Sheds | /vinyl-siding-for-storage-shed/ |

### Other/Utility Pages
| # | Page | Staging URL |
|---|------|-------------|
| 68 | Inventory Page 2 | /inventory/page/2/ |
| 69 | 8x12 Shed Size (alt URL) | /shedsize8x12/ |
| 70 | Individual Inventory Items | /inventory/{item-slug}/ |

---

## Detailed Per-Page QA Checklist

---

### PAGE 1: Homepage ( / )
**Production:** https://www.beachybarns.com/

**Content Check:**
- [ ] Hero banner/slider loads correctly with images
- [ ] Headline text is correct (not placeholder/lorem ipsum)
- [ ] All navigation menu items are present and link to correct pages
- [ ] "Since 1982" or founding year is displayed
- [ ] Shed style thumbnails/cards display correctly (10+ styles)
- [ ] Call-to-action buttons work (Free Quote, Contact, etc.)
- [ ] Phone number is visible and correct: (614) 873-4193
- [ ] Address shows: 8720 Amish Pike, Plain City, OH 43064

**Design Check:**
- [ ] Page is NOT blank (has substantial content beyond header/footer)
- [ ] All images load (no broken image icons)
- [ ] Mobile responsive - check at 375px, 768px, 1024px widths
- [ ] No horizontal scrollbar on mobile
- [ ] Footer renders correctly with all links
- [ ] No overlapping elements or layout shifts

**Technical Check:**
- [ ] No PHP errors/warnings visible on page
- [ ] No "Error establishing a database connection"
- [ ] Page title is descriptive (not "Just another WordPress site")
- [ ] Meta description is present
- [ ] No mixed content warnings (HTTP resources on HTTPS)
- [ ] Page loads in under 5 seconds

---

### PAGE 2: Storage Sheds ( /storage-sheds/ )
**Production:** https://www.beachybarns.com/storage-sheds/

**Content Check:**
- [ ] Page has introductory text about shed styles offered
- [ ] All shed style cards/thumbnails are present:
  - [ ] Gable
  - [ ] Quaker
  - [ ] Cape Cod
  - [ ] Classic
  - [ ] Mini Barn
  - [ ] Cottage
  - [ ] Cabin
  - [ ] Retreat
  - [ ] Highwall
  - [ ] Premier Highwall
  - [ ] Modern Studio
  - [ ] Shed Bar
  - [ ] Custom
- [ ] Each card links to its correct sub-page
- [ ] Images load for each shed style

**Design Check:**
- [ ] Grid/card layout is consistent and aligned
- [ ] Page is NOT blank (should have 10+ style cards with images)
- [ ] Hover effects work on cards (if applicable)
- [ ] Mobile: cards stack properly in single column

**Technical Check:**
- [ ] All shed style links resolve (no 404s)
- [ ] No broken images
- [ ] No PHP errors visible

---

### PAGES 14-26: Individual Shed Style Pages

**Check EACH of these pages:**
- /storage-sheds/gable-sheds/
- /storage-sheds/quaker/
- /storage-sheds/cape-cod-sheds/
- /storage-sheds/classic/
- /storage-sheds/mini-barn/
- /storage-sheds/cottage/
- /storage-sheds/cabin/
- /storage-sheds/retreat/
- /storage-sheds/highwall/
- /storage-sheds/premier-highwall/
- /storage-sheds/modern-studio/
- /storage-sheds/shed-bar/
- /storage-sheds/custom/

**For EACH shed style page:**
- [ ] Page is NOT blank (has real descriptive content, not just header/footer)
- [ ] Shed style name matches the URL/page
- [ ] Description text is present (not placeholder)
- [ ] High-quality shed photos load correctly
- [ ] Photo gallery/slider works (if present)
- [ ] Sizing information or available sizes listed
- [ ] Features/specs are listed
- [ ] CTA button present (Get a Quote / View Inventory / 3D Builder)
- [ ] Link to 3-D Shed Builder works (if present)
- [ ] Breadcrumb navigation is correct
- [ ] No broken internal links
- [ ] No PHP errors visible on page

**Common Issues to Watch For:**
- Blank/stub pages with only a title and no body content
- Missing images (broken image icons)
- Wrong shed photos on wrong style page
- Dead links to 3D builder tool
- "Coming Soon" or placeholder text

---

### PAGE 3: Shed Sizes ( /shed-sizes/ )
**Production:** https://www.beachybarns.com/shed-sizes/

**Content Check:**
- [ ] Overview text about available sizes
- [ ] Grid/list of all available sizes with links:
  - [ ] 6x6, 6x8, 8x10, 8x12, 10x10, 10x12, 10x14, 10x16
  - [ ] 12x16, 12x20, 12x24, 14x20, 14x24, 16x28
- [ ] Each size links to its detail page

**Design Check:**
- [ ] Page is NOT blank
- [ ] Size cards/links are visually organized
- [ ] Mobile responsive layout

---

### PAGES 29-42: Individual Shed Size Pages

**Check EACH size page:**
- /shed-sizes/6x6-sheds/
- /shed-sizes/6x8-sheds/
- /shed-sizes/8x10-sheds/
- /shed-sizes/8x12-sheds/
- /shed-sizes/10x10-sheds/
- /shed-sizes/10x12-sheds-in-ohio/
- /shed-sizes/10x14-sheds/
- /shed-sizes/10x16-sheds/
- /shed-sizes/12x16-sheds/
- /shed-sizes/12x20-sheds/
- /shed-sizes/12x24-sheds/
- /shed-sizes/14x20-sheds/
- /shed-sizes/14x24-sheds/
- /shed-sizes/16x28-sheds/

**For EACH size page:**
- [ ] Page is NOT blank
- [ ] Size dimensions are correctly stated in content
- [ ] Description text explains use cases for this size
- [ ] Available styles for this size are listed
- [ ] Photos of sheds in this size are present and load
- [ ] Starting price or link to pricing is present (if applicable)
- [ ] CTA to get a quote or configure in 3D builder
- [ ] No broken links or images

---

### PAGES 27-28: Garage Pages

#### /garages/highwall-garage-shed/
- [ ] Page is NOT blank
- [ ] Highwall garage photos load correctly
- [ ] Description mentions 6' loft, 2x8 treated floors
- [ ] Overhead door information present
- [ ] Pricing or quote CTA present
- [ ] Free delivery info (50 miles from Plain City)

#### /garages/gable-garage/
- [ ] Page is NOT blank
- [ ] Gable garage photos load
- [ ] Specifications listed
- [ ] CTA present

---

### PAGE 5: Inventory ( /inventory/ )
**Production:** https://www.beachybarns.com/inventory/

**Content Check:**
- [ ] Page displays in-stock sheds/buildings
- [ ] Each inventory item shows: photo, size, style, price, stock number
- [ ] "Ready to deliver" messaging present
- [ ] Pagination works (check /inventory/page/2/, /inventory/page/3/, etc.)
- [ ] Individual inventory items link to detail pages

**Design Check:**
- [ ] Product grid/list layout is consistent
- [ ] All product images load
- [ ] Filtering/sorting works (if present)
- [ ] Mobile: product cards stack properly
- [ ] No empty/blank product cards

**Technical Check:**
- [ ] Pagination links work (not 404)
- [ ] Individual inventory item pages load (not 404)
- [ ] No PHP errors

---

### PAGE 6: Rent-to-Own ( /rent-to-own/ )
**Production:** https://www.beachybarns.com/rent-to-own/

**Content Check:**
- [ ] Page explains rent-to-own program
- [ ] 3-step process is clearly laid out:
  1. Choose size and style
  2. Pay first month's rent, get delivery
  3. Make 36 equal monthly payments
- [ ] "No credit check required" messaging present
- [ ] Payment calculation formula (cash price / 21.6)
- [ ] Early payoff info (60% of remaining payments)
- [ ] Return policy mentioned

**Design Check:**
- [ ] Page is NOT blank
- [ ] Step graphics/icons render
- [ ] CTA to request a quote
- [ ] Mobile responsive

---

### PAGE 7: On-Site Build ( /on-site-build/ )
- [ ] Page is NOT blank
- [ ] Explains on-site construction process
- [ ] Size limitations mentioned (over 14' wide = on-site only, max 16x50, min 6x8)
- [ ] Photos of on-site build process
- [ ] CTA present

---

### PAGE 8: Shed Options ( /shed-options/ )
**Production:** https://www.beachybarns.com/shed-options/

- [ ] Page lists customization options:
  - [ ] Windows
  - [ ] Lofts
  - [ ] Shelves/workbenches
  - [ ] Cupolas
  - [ ] Shutters/flower boxes
  - [ ] Ramps
  - [ ] Siding options (Duratemp, vinyl)
  - [ ] Roofing options (shingles, metal)
  - [ ] Porch add-ons
- [ ] Images show each option
- [ ] Not blank/stub page

---

### PAGE 9: Download a Catalog ( /download-a-catalog/ )
- [ ] Page has description of the catalog
- [ ] Download form or direct download link works
- [ ] PDF actually downloads (not 404 or broken)
- [ ] Form validation works if form present
- [ ] Not blank/stub page

---

### PAGE 10: Site Preparation ( /site-preparation/ )
- [ ] Page explains how to prepare property for shed delivery
- [ ] Foundation options discussed
- [ ] Clear, helpful content for customers
- [ ] Images/diagrams present
- [ ] Not blank/stub page

---

### PAGES 43-60: Location Pages

**Check EACH location page. All follow same template:**
- /locations/sheds-in-columbus-ohio/
- /locations/sheds-in-dayton-ohio/
- /locations/storage-sheds-in-fairborn-ohio/
- /locations/sheds-in-springfield-ohio/
- /locations/storage-buildings-in-cincinnati-ohio/
- /locations/sheds-in-dublin-ohio/
- /locations/storage-buildings-in-kettering-ohio/
- /locations/backyard-sheds-in-huber-heights-ohio/
- /locations/storage-buildings-in-beaver-creek-ohio/
- /locations/storage-buildings-in-lancaster-ohio/
- /locations/storage-buildings-in-newark-ohio/
- /locations/sheds-for-sale-westerville-ohio/
- /locations/sheds-for-sale-in-worthington-oh/
- /locations/sheds-for-sale-in-grove-city-oh/
- /locations/sheds-for-sale-in-blacklick-estates-ohio/
- /locations/storage-buildings-delaware/
- /locations/sheds-in-indian-lake-ohio/
- /locations/prefab-buildings-in-marysville-ohio/

**For EACH location page:**
- [ ] Page is NOT blank (needs substantial local content)
- [ ] City name is correct in title, heading, and body text
- [ ] Content is unique (not exact duplicate of other location pages)
- [ ] Lists shed styles available (Gable, Quaker, Cape Cod, etc.)
- [ ] Mentions on-site build availability
- [ ] Mentions delivery to this area
- [ ] Rent-to-own mention
- [ ] Photos present and loading
- [ ] CTA to get a quote
- [ ] No PHP errors
- [ ] All internal links work

**Common Location Page Issues:**
- Blank/stub pages with just the city name and no content
- Copy-pasted content with wrong city name left in
- Missing or broken images
- Broken internal links to shed style pages

---

### PAGE 11: Tips & Stories Blog ( /tips-stories/ )
- [ ] Blog index loads with list of articles
- [ ] Each article card has: title, excerpt, featured image
- [ ] Article links work (not 404)
- [ ] Pagination works if multiple pages

### Blog Post Pages (61-67):
**Check each post is NOT blank and has real content:**
- [ ] /tips-stories/the-home-farm/
- [ ] /tips-stories/deciding-what-size-shed-you-need/
- [ ] /tips-stories/8-x-10-storage-shed-pros-and-cons/
- [ ] /10x10-sheds-everything-you-need-to-know/
- [ ] /tips-stories/10x12-sheds/
- [ ] /vinyl-siding-for-storage-shed/

---

### Contact / About / Quote Pages
- [ ] /contact/ - Form works, all fields validate, submission succeeds
- [ ] /about/ - Company history, team info, not blank
- [ ] Free quote form - Fields work, required validation, submission works

---

## Global Checks (Apply to ALL Pages)

### Navigation
- [ ] Main menu is consistent across all pages
- [ ] All menu items link to correct pages
- [ ] Mobile hamburger menu opens/closes properly
- [ ] Submenu dropdowns work on desktop
- [ ] Logo links back to homepage
- [ ] No broken links in navigation

### Footer
- [ ] Footer appears on all pages
- [ ] Address: 8720 Amish Pike, Plain City, OH 43064
- [ ] Phone: (614) 873-4193
- [ ] Social media links work
- [ ] Footer navigation links work
- [ ] Copyright year is current (2026)

### Mobile Responsiveness (Test Each Page)
- [ ] No horizontal scrollbar at any width
- [ ] Text is readable without zooming
- [ ] Buttons/links are tap-friendly (min 44px target)
- [ ] Images scale appropriately
- [ ] Navigation works on mobile
- [ ] Forms are usable on mobile

### Performance
- [ ] All pages load in under 5 seconds
- [ ] Images are optimized (no 5MB+ photos)
- [ ] No unnecessary redirects

### SEO
- [ ] Every page has a unique `<title>` tag
- [ ] Every page has a meta description
- [ ] Staging site has `noindex` meta tag (to prevent search engine indexing)
- [ ] Canonical URLs point to staging (or production if intentional)
- [ ] All images have alt text

### Security
- [ ] SSL certificate is valid (https works)
- [ ] No mixed content warnings
- [ ] Forms submit over HTTPS
- [ ] WordPress login works
- [ ] wp-admin is accessible with credentials

---

## Priority Issues to Watch For

1. **BLANK PAGES** - Pages that show only header + footer with no body content. These are the most visible issues to check first.

2. **404 ERRORS** - Pages that exist on production but return "Page Not Found" on staging. May indicate incomplete migration.

3. **BROKEN IMAGES** - Hardcoded production URLs in image paths that don't resolve on staging.

4. **HARDCODED URLS** - Links pointing to `www.beachybarns.com` instead of `beachybarnstaging.dreamhosters.com`. WordPress often hardcodes the site URL in the database.

5. **PHP/DATABASE ERRORS** - Visible error messages like "Error establishing a database connection" or PHP warnings.

6. **MISSING PLUGINS** - If plugins weren't migrated, pages using page builders (Elementor, WPBakery, etc.) may appear blank or broken.

7. **WRONG STAGING URL** - Search-and-replace may not have caught all production URLs in the database.

---

*Report generated: 2026-02-06*
*Run the automated crawler for real-time broken link/image detection*
