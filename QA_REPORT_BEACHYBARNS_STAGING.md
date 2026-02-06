# Beachy Barns Staging Site - Full QA Report & Checklist

**Staging URL:** https://beachybarnstaging.dreamhosters.com
**Production URL:** https://www.beachybarns.com
**Prepared for:** Web Design Team
**Date:** 2026-02-06
**Total known pages:** 269+ (190+ discovered via search index, remainder discoverable via automated crawler)

---

## How to Use This Report

This report maps **every known page** on the Beachy Barns website. For each page:
1. Open the staging URL in your browser
2. Cross-reference against the production site
3. Check each bullet point
4. Mark items as PASS / FAIL / N/A

**IMPORTANT: Run the automated crawler to find ALL 269 pages** (including inventory items, pagination, and unlisted location pages that search engines didn't surface):
```bash
pip install requests beautifulsoup4 lxml
python src/staging_qa_report.py https://beachybarnstaging.dreamhosters.com/ \
  --wp-user "Jonathan Dominise" --wp-pass "JDominise321!" \
  --max-pages 500 -o automated_qa_report.md --json qa_report.json
```

---

## Complete Site Map (190+ Pages Discovered)

### A. Core / Main Pages (17 pages)

| # | Page | Staging URL | Production URL |
|---|------|-------------|----------------|
| 1 | Homepage | / | beachybarns.com/ |
| 2 | About Us | /about-us/ | beachybarns.com/about-us/ |
| 3 | Contact Us | /contact-us/ | beachybarns.com/contact-us/ |
| 4 | Testimonials | /testimonials/ | beachybarns.com/testimonials/ |
| 5 | Storage Sheds (parent) | /storage-sheds/ | beachybarns.com/storage-sheds/ |
| 6 | Shed Sizes (parent) | /shed-sizes/ | beachybarns.com/shed-sizes/ |
| 7 | Garages (parent) | /garages/ | beachybarns.com/garages/ |
| 8 | Inventory | /inventory/ | beachybarns.com/inventory/ |
| 9 | Rent-to-Own | /rent-to-own/ | beachybarns.com/rent-to-own/ |
| 10 | On-Site Build | /on-site-build/ | beachybarns.com/on-site-build/ |
| 11 | Shed Options | /shed-options/ | beachybarns.com/shed-options/ |
| 12 | Download a Catalog | /download-a-catalog/ | beachybarns.com/download-a-catalog/ |
| 13 | Site Preparation | /site-preparation/ | beachybarns.com/site-preparation/ |
| 14 | Shed Uses / Inspiration Room | /shed-uses/ | beachybarns.com/shed-uses/ |
| 15 | Shed Interior Ideas | /shed-interior-ideas/ | beachybarns.com/shed-interior-ideas/ |
| 16 | Custom Sheds | /custom-sheds/ | beachybarns.com/custom-sheds/ |
| 17 | Locations (parent) | /locations/ | beachybarns.com/locations/ |

### B. Shed Style Pages (13 pages)

| # | Page | Staging URL |
|---|------|-------------|
| 16 | Gable Sheds | /storage-sheds/gable-sheds/ |
| 17 | Quaker Sheds | /storage-sheds/quaker/ |
| 18 | Cape Cod Sheds | /storage-sheds/cape-cod-sheds/ |
| 19 | Classic Sheds | /storage-sheds/classic/ |
| 20 | Mini Barn | /storage-sheds/mini-barn/ |
| 21 | Cottage Sheds | /storage-sheds/cottage/ |
| 22 | Cabin Sheds | /storage-sheds/cabin/ |
| 23 | Retreat (Sheds with Porches) | /storage-sheds/retreat/ |
| 24 | Highwall Sheds | /storage-sheds/highwall/ |
| 25 | Premier Highwall | /storage-sheds/premier-highwall/ |
| 26 | Modern Studio | /storage-sheds/modern-studio/ |
| 27 | Shed Bar | /storage-sheds/shed-bar/ |
| 28 | Custom Sheds | /storage-sheds/custom/ |

### C. Garage Pages (2 pages)

| # | Page | Staging URL |
|---|------|-------------|
| 29 | Highwall Garage | /garages/highwall-garage-shed/ |
| 30 | Gable Garage | /garages/gable/ |

### D. Shed Size Pages (30+ pages)

| # | Page | Staging URL |
|---|------|-------------|
| 31 | 6x6 Sheds | /shed-sizes/6x6-sheds/ |
| 32 | 6x8 Sheds | /shed-sizes/6x8-sheds/ |
| 33 | 6x10 Sheds | /shed-sizes/6x10-sheds/ |
| 34 | 6x12 Sheds | /shed-sizes/6x12-sheds/ |
| 35 | 8x8 Sheds | /shed-sizes/8x8-sheds/ |
| 36 | 8x10 Sheds | /shed-sizes/8x10-sheds-in-ohio/ |
| 37 | 8x12 Sheds | /shed-sizes/8x12-sheds/ |
| 38 | 8x14 Sheds | /shed-sizes/8x14-sheds-in-ohio/ |
| 39 | 8x16 Sheds | /shed-sizes/8x16-sheds/ |
| 40 | 10x10 Sheds | /shed-sizes/10x10-sheds/ |
| 41 | 10x12 Sheds | /shed-sizes/10x12-sheds-in-ohio/ |
| 42 | 10x14 Sheds | /shed-sizes/10x14-sheds/ |
| 43 | 10x16 Sheds | /shed-sizes/10x16-sheds/ |
| 44 | 10x18 Sheds | /shed-sizes/10x18-sheds/ |
| 45 | 10x20 Sheds | /shed-sizes/10x20-sheds/ |
| 46 | 12x14 Sheds | /shed-sizes/12x14-sheds/ |
| 47 | 12x16 Sheds | /shed-sizes/12x16-sheds-in-ohio/ |
| 48 | 12x18 Sheds | /shed-sizes/12x18-sheds/ |
| 49 | 12x20 Sheds | /shed-sizes/12x20-sheds/ |
| 50 | 12x24 Sheds | /shed-sizes/12x24-sheds/ |
| 51 | 14x20 Sheds | /shed-sizes/14x20-sheds/ |
| 52 | 14x24 Sheds | /shed-sizes/14x24-sheds/ |
| 53 | 14x32 Sheds | /shed-sizes/14x32-sheds/ |
| 54 | 16x12 Sheds | /shed-sizes/16x12-sheds/ |
| 55 | 16x18 Sheds | /shed-sizes/16x18-sheds/ |
| 56 | 16x22 Sheds | /shed-sizes/16x22-sheds/ |
| 57 | 16x24 Sheds | /shed-sizes/16x24-sheds/ |
| 58 | 16x28 Sheds | /shed-sizes/16x28-sheds/ |
| 59 | 16x30 Sheds | /shed-sizes/16x30-sheds/ |
| 60 | 16x40 Shed | /shed-sizes/16x40-shed/ |
| 61 | 16x50 Sheds | /shed-sizes/16x50-sheds/ |
| 62 | 8x12 (alt URL) | /shedsize8x12/ |

**NOTE:** The production Shed Sizes parent page lists sizes from small (6x6) to large (16x32 max). There may be additional size pages (e.g., 8x16, 12x12, 12x22, 14x14, 14x16, 14x18, 14x28, 16x20, 16x26, 16x32, 16x36, 16x44, 16x48) not surfaced by search. The automated crawler will find all of them.

### E. Location Pages (25+ confirmed, likely 100+ total)

| # | Page | Staging URL |
|---|------|-------------|
| 63 | Columbus | /locations/sheds-in-columbus-ohio/ |
| 64 | Dayton | /locations/sheds-in-dayton-ohio/ |
| 65 | Fairborn | /locations/storage-sheds-in-fairborn-ohio/ |
| 66 | Springfield | /locations/sheds-in-springfield-ohio/ |
| 67 | Cincinnati | /locations/storage-buildings-in-cincinnati-ohio/ |
| 68 | Dublin | /locations/sheds-in-dublin-ohio/ |
| 69 | Kettering | /locations/storage-buildings-in-kettering-ohio/ |
| 70 | Huber Heights | /locations/backyard-sheds-in-huber-heights-ohio/ |
| 71 | Beaver Creek | /locations/storage-buildings-in-beaver-creek-ohio/ |
| 72 | Lancaster | /locations/storage-buildings-in-lancaster-ohio/ |
| 73 | Newark | /locations/storage-buildings-in-newark-ohio/ |
| 74 | Westerville | /locations/sheds-for-sale-westerville-ohio/ |
| 75 | Worthington | /locations/sheds-for-sale-in-worthington-oh/ |
| 76 | Grove City | /locations/sheds-for-sale-in-grove-city-oh/ |
| 77 | Blacklick Estates | /locations/sheds-for-sale-in-blacklick-estates-ohio/ |
| 78 | Delaware | /locations/storage-buildings-delaware/ |
| 79 | Indian Lake | /locations/sheds-in-indian-lake-ohio/ |
| 80 | Marysville | /locations/prefab-buildings-in-marysville-ohio/ |
| 81 | Vandalia | /locations/storage-buildings-in-vandalia-ohio/ |
| 82 | Whitehall | /locations/sheds-for-sale-in-whitehall-oh/ |
| 83 | Gahanna | /locations/sheds-for-sale-in-gahanna-ohio/ |
| 84 | Urbana | /locations/sheds-for-sale-in-urbana-ohio/ |
| 85 | Lincoln Village | /locations/sheds-for-sale-in-lincoln-village-oh/ |
| 86 | New Albany | /locations/sheds-in-new-albany-ohio/ |
| 87 | Upper Arlington | /locations/sheds-for-sale-in-upper-arlington-ohio/ |

**NOTE:** With 269+ total pages and ~30 shed sizes, ~13 shed styles, ~15 blog posts, ~15 core pages, and ~18 inventory items, there are likely **100-150+ location pages** covering Ohio cities. The automated crawler will discover all of them. Common cities to check include: Hilliard, Pataskala, Pickerington, Reynoldsburg, London, Upper Arlington, Powell, Xenia, Troy, Piqua, Sidney, Circleville, Marion, Findlay, Ashland, Mansfield, Zanesville, Chillicothe, and many more.

### F. Blog / Tips & Stories Pages (22+ pages)

| # | Page | Staging URL |
|---|------|-------------|
| 87 | Tips & Stories Index | /tips-stories/ |
| 88 | The Home Farm | /tips-stories/the-home-farm/ |
| 89 | This Old Barn | /tips-stories/this-old-barn/ |
| 90 | Deciding What Size Shed | /tips-stories/deciding-what-size-shed-you-need/ |
| 91 | 8x10 Shed Pros & Cons | /tips-stories/8-x-10-storage-shed-pros-and-cons/ |
| 92 | 10x10 Sheds Everything to Know | /10x10-sheds-everything-you-need-to-know/ |
| 93 | 10x12 Sheds Guide | /tips-stories/10x12-sheds/ |
| 94 | Vinyl Siding for Sheds | /tips-stories/vinyl-siding-for-storage-shed/ |
| 95 | Shed Permits in Ohio | /tips-stories/shed-permits-in-ohio/ |
| 96 | Garden Shed Insulation (Spray Foam) | /tips-stories/garden-shed-insulation-spray-foam/ |
| 97 | Best Shed Foundations | /tips-stories/best-shed-foundations/ |
| 98 | Outdoor Kitchen Sheds Guide | /tips-stories/outdoor-kitchen-shed-ultimate-guide/ |
| 99 | 10 Man Cave Shed Ideas | /tips-stories/10-superman-cave-shed-ideas/ |
| 100 | 12 Shed Bar Ideas | /tips-stories/12-shed-bar-ideas-2021/ |
| 101 | Sheds With Porches (17 Ideas) | /tips-stories/a-porch-trait-of-sheds/ |
| 102 | She Sheds Guide | /tips-stories/she-sheds/ |
| 103 | Hangout Shed Ideas | /tips-stories/a-hangout-shed-for-a-backyard-vacation-spot/ |
| 104 | Home Office Sheds | /tips-stories/home-office-sheds/ |
| 105 | Gym Shed Guide | /tips-stories/quick-guide-to-an-affordable-gym-shed/ |
| 106 | Shed Interior Ideas (blog ver.) | /tips-stories/shed-interior-ideas/ |
| 107 | How to Top Off Your Shed (Roofing) | /tips-stories/how-to-top-off-your-new-shed/ |
| 108 | Floored! (Shed Flooring) | /tips-stories/floored/ |
| 109 | Kitschen Bakery Farm Stand Shed | /tips-stories/kitschen-bakery-farm-stand-shed/ |
| 110 | Jefferson Street Oasis Gardens | /tips-stories/jefferson-street-oasis-customer-story/ |
| 111 | Prefab Pool House Ideas | /tips-stories/prefab-pool-house-ideas/ |
| 112 | Prefab Cabin Getaway | /tips-stories/prefab-cabin-getaway/ |

### G. Inventory Item Pages (20+ confirmed, likely more)

| # | Page | Staging URL |
|---|------|-------------|
| 109 | Inventory Main | /inventory/ |
| 110 | Inventory Page 2 | /inventory/page/2/ |
| 111 | Inventory Page 3+ | /inventory/page/3/ (check for more) |
| 112 | 10x20 Cabin #15945 | /inventory/10x20-cabin-15945/ |
| 113 | 8x12 Cabin #15143 | /inventory/8x12-cabin-15143/ |
| 114 | 8x12 Cape Cod #15372 | /inventory/8x12-cape-cod-15372/ |
| 115 | 8x12 Mini Barn #15375 | /inventory/8x12-mini-barn-15375/ |
| 116 | 10x20 Cottage #14923 | /inventory/10x20-cottage-2-14923/ |
| 117 | 8x8 Mini Barn #13086 | /inventory/8x8-mini-barn-13086/ |
| 118 | 10x16 Quaker #15411 | /inventory/10x16-quaker-15411/ |
| 119 | 10x20 Modern Studio #14947 | /inventory/10x20-modern-studio-14947/ |
| 120 | 8x10 Mini Barn #15009 | /inventory/8x10-mini-barn-15009/ |
| 121 | 10x12 Modern Studio #16174 | /inventory/10x12-modern-studio-16174/ |
| 122 | 12x16 Cottage #15882 | /inventory/12x16-cottage-15882/ |
| 123 | 10x12 Cape Cod #16273 | /inventory/10x12-cape-cod-16273/ |
| 124 | 14x24 Gable #16262 | /inventory/14x24-gable-16262/ |
| 125 | 12x24 Gable Garage #16319 | /inventory/12x24-gable-garage-16319/ |
| 126 | 12x20 Cape Cod #16302 | /inventory/12x20-cape-cod-3-16302/ |
| 127 | 14x28 Gable Garage #16259 | /inventory/14x28-gable-garage-16259/ |
| 128 | 12x20 Cape Cod #16300 | /inventory/12x20-cape-cod-2-16300/ |
| 129 | 10x20 Modern Studio #16704 | /inventory/1014-gable-16704/ |

**NOTE:** Inventory items are dynamic - items sell and new ones are added. Check ALL items visible on /inventory/ and its paginated pages.

---

## Detailed Per-Page QA Checklist

### A. CORE PAGES

---

#### 1. Homepage ( / )
- [ ] Hero banner/slider loads with high-quality images
- [ ] "Building Quality Sheds In Ohio Since 1982" headline or similar
- [ ] All navigation menu items present and working
- [ ] 10+ shed style thumbnails/cards display correctly
- [ ] CTA buttons work (Free Quote, Design in 3D, etc.)
- [ ] Phone number visible: (614) 873-4193
- [ ] Address: 8720 Amish Pike, Plain City, OH 43064
- [ ] Winter/Seasonal sale banners display if applicable
- [ ] 10-year warranty mentioned
- [ ] Free delivery (50 miles) mentioned
- [ ] NOT blank - substantial hero + content sections
- [ ] All images load, no broken icons
- [ ] Mobile responsive at 375px, 768px, 1024px
- [ ] Footer complete with address, phone, social, links
- [ ] No PHP errors visible
- [ ] Page title is NOT "Just another WordPress site"

---

#### 2. About Us ( /about-us/ )
- [ ] Company history (Lawrence Beachy, founded 1982, family farm)
- [ ] Plain City, Ohio location mentioned
- [ ] Team/family photos load
- [ ] NOT blank page
- [ ] No placeholder text

---

#### 3. Contact Us ( /contact-us/ )
- [ ] Address: 8720 Amish Pike, Plain City, OH 43064
- [ ] Phone: (614) 873-4193
- [ ] Hours: Mon-Fri 8AM-5PM, Sat 10AM-2PM
- [ ] Contact form present and functional
- [ ] Form submission works (test submit)
- [ ] Form validation works (required fields)
- [ ] Map/directions present
- [ ] NOT blank page

---

#### 4. Testimonials ( /testimonials/ )
- [ ] Customer reviews display
- [ ] Review content is readable
- [ ] Star ratings show (if applicable)
- [ ] NOT blank page
- [ ] No broken review widgets

---

#### 5. Storage Sheds ( /storage-sheds/ )
- [ ] Introduction text about shed styles
- [ ] ALL 13 shed style cards present with images:
  - [ ] Gable, Quaker, Cape Cod, Classic, Mini Barn, Cottage
  - [ ] Cabin, Retreat, Highwall, Premier Highwall
  - [ ] Modern Studio, Shed Bar, Custom
- [ ] Each card links to correct sub-page (no 404s)
- [ ] All card images load
- [ ] 10-year warranty badge
- [ ] Free delivery mention
- [ ] Grid layout consistent, mobile responsive

---

#### 6. Shed Sizes ( /shed-sizes/ )
- [ ] Overview text about size categories (small/mid/large)
- [ ] Small: 6x6 through 8x12
- [ ] Mid: 8x14 through 12x20
- [ ] Large: 12x24 through 16x50 (max)
- [ ] Most popular: 10x16 mentioned
- [ ] All size links resolve (no 404s)
- [ ] NOT blank page

---

#### 7. Garages ( /garages/ )
- [ ] Gable Garage and Highwall Garage listed
- [ ] Links to sub-pages work
- [ ] NOT blank page

---

#### 8. Inventory ( /inventory/ )
- [ ] Product grid displays in-stock sheds
- [ ] Each item shows: photo, size, style, price, stock number
- [ ] Sale prices/clearance tagging works
- [ ] "Ready to deliver" messaging
- [ ] Pagination works (/inventory/page/2/, page/3/, etc.)
- [ ] Individual item pages load when clicked
- [ ] Product images load
- [ ] Filtering/sorting works
- [ ] Mobile: cards stack properly

---

#### 9. Rent-to-Own ( /rent-to-own/ )
- [ ] 3-step process explained:
  1. Choose size and style
  2. Pay first month's rent
  3. Make 36 monthly payments
- [ ] No credit check required
- [ ] Payment formula: cash price / 21.6
- [ ] Early payoff: 60% of remaining
- [ ] Return policy noted
- [ ] CTA to request quote
- [ ] NOT blank page

---

#### 10. On-Site Build ( /on-site-build/ )
- [ ] Construction process explained
- [ ] Over 14' wide = on-site only
- [ ] Over 12'3" tall = on-site only
- [ ] Max: 16x50, Min: 6x8
- [ ] Request a Quote form or 3D Builder link
- [ ] Photos of on-site construction
- [ ] NOT blank page

---

#### 11. Shed Options ( /shed-options/ )
- [ ] Customization options listed with images:
  - [ ] Windows, Lofts, Shelves/workbenches
  - [ ] Cupolas, Shutters, Flower boxes
  - [ ] Ramps, Siding (Duratemp/vinyl), Roofing (shingles/metal)
  - [ ] Porch add-ons, Door/window placement
- [ ] NOT blank page

---

#### 12. Download a Catalog ( /download-a-catalog/ )
- [ ] Description of what the catalog contains
- [ ] Download form or direct link works
- [ ] PDF actually downloads
- [ ] NOT blank page

---

#### 13. Site Preparation ( /site-preparation/ )
- [ ] Foundation options explained
- [ ] Gravel pad, concrete slab, poured pier options
- [ ] Images/diagrams present
- [ ] NOT blank page

---

#### 14. Shed Uses / Inspiration Room ( /shed-uses/ )
- [ ] Various use cases shown: cabin, tiny home, pool house, bar, office
- [ ] Photos for each use case
- [ ] NOT blank page

---

#### 15. Shed Interior Ideas ( /shed-interior-ideas/ )
- [ ] Interior design ideas: shelving, hooks, home office, game shed, bar, man cave
- [ ] Photos present
- [ ] NOT blank page

---

### B. SHED STYLE PAGES (13 pages)

**Check EACH of these pages for the following:**

| URL | Expected Title |
|-----|---------------|
| /storage-sheds/gable-sheds/ | Gable Sheds |
| /storage-sheds/quaker/ | Quaker Sheds |
| /storage-sheds/cape-cod-sheds/ | Cape Cod Sheds |
| /storage-sheds/classic/ | Classic Sheds |
| /storage-sheds/mini-barn/ | Mini Barn |
| /storage-sheds/cottage/ | Cottage Sheds |
| /storage-sheds/cabin/ | Cabin Sheds |
| /storage-sheds/retreat/ | Retreat / Sheds With Porches |
| /storage-sheds/highwall/ | Highwall Sheds |
| /storage-sheds/premier-highwall/ | Premier Highwall |
| /storage-sheds/modern-studio/ | Modern Studio |
| /storage-sheds/shed-bar/ | Shed Bar |
| /storage-sheds/custom/ | Custom Sheds |

**For EACH:**
- [ ] Page is NOT blank (has paragraphs of descriptive content)
- [ ] Shed style name matches the URL
- [ ] Multiple high-quality photos load
- [ ] Photo gallery/slider works
- [ ] Available sizes listed
- [ ] Features/specs listed
- [ ] Standard features mentioned (2x4 studs, treated skids, etc.)
- [ ] CTA: "Get a Quote" / "Design in 3D Builder" / "View Inventory"
- [ ] 3-D Shed Builder link works
- [ ] Free delivery (50 miles) mentioned
- [ ] Rent-to-own option mentioned
- [ ] Breadcrumb navigation correct
- [ ] No broken links or images
- [ ] No PHP errors visible
- [ ] No wrong shed photos for the style

---

### C. GARAGE PAGES (2 pages)

#### /garages/highwall-garage-shed/
- [ ] Highwall garage photos load
- [ ] 6' loft standard, 2x8 treated floor
- [ ] Overhead door info
- [ ] Free delivery (50 miles)
- [ ] On-site build option ($500 extra)
- [ ] 3D Builder + Request Quote CTAs
- [ ] NOT blank

#### /garages/gable/
- [ ] Gable garage photos load
- [ ] Specifications listed
- [ ] Free delivery (50 miles)
- [ ] Request a Quote + Design in 3D CTAs
- [ ] Rent-to-own (delivered preassembled only)
- [ ] NOT blank

---

### D. SHED SIZE PAGES (30+ pages)

**Check EACH URL below. For each page verify:**
- [ ] Page is NOT blank
- [ ] Correct size dimensions stated in heading + body
- [ ] Description explains use cases
- [ ] Available styles for this size listed
- [ ] Photos of sheds in this size
- [ ] 3D Builder link works
- [ ] CTA to get a quote
- [ ] No broken links or images

**All shed size URLs:**
```
/shed-sizes/6x6-sheds/
/shed-sizes/6x8-sheds/
/shed-sizes/6x10-sheds/
/shed-sizes/6x12-sheds/
/shed-sizes/8x8-sheds/
/shed-sizes/8x10-sheds-in-ohio/
/shed-sizes/8x12-sheds/
/shed-sizes/8x14-sheds-in-ohio/
/shed-sizes/8x16-sheds/
/shed-sizes/10x10-sheds/
/shed-sizes/10x12-sheds-in-ohio/
/shed-sizes/10x14-sheds/
/shed-sizes/10x16-sheds/
/shed-sizes/10x18-sheds/
/shed-sizes/10x20-sheds/
/shed-sizes/12x14-sheds/
/shed-sizes/12x16-sheds-in-ohio/
/shed-sizes/12x18-sheds/
/shed-sizes/12x20-sheds/
/shed-sizes/12x24-sheds/
/shed-sizes/14x20-sheds/
/shed-sizes/14x24-sheds/
/shed-sizes/14x32-sheds/
/shed-sizes/16x12-sheds/
/shed-sizes/16x18-sheds/
/shed-sizes/16x22-sheds/
/shed-sizes/16x24-sheds/
/shed-sizes/16x28-sheds/
/shed-sizes/16x30-sheds/
/shed-sizes/16x40-shed/
/shed-sizes/16x50-sheds/
/shedsize8x12/
/shedsize10x16/
/shedsize10x20/
/shedsize12x16/
/shedsize12x28/
```

**Additional sizes that may exist (check these):**
```
/shed-sizes/12x12-sheds/
/shed-sizes/12x22-sheds/
/shed-sizes/14x14-sheds/
/shed-sizes/14x16-sheds/
/shed-sizes/14x18-sheds/
/shed-sizes/14x28-sheds/
/shed-sizes/16x20-sheds/
/shed-sizes/16x26-sheds/
/shed-sizes/16x32-sheds/
/shed-sizes/16x36-sheds/
/shed-sizes/16x44-sheds/
/shed-sizes/16x48-sheds/
```

---

### E. LOCATION PAGES (25 confirmed + 80-130 more expected)

**Confirmed location pages (check each):**
```
/locations/sheds-in-columbus-ohio/
/locations/sheds-in-dayton-ohio/
/locations/storage-sheds-in-fairborn-ohio/
/locations/sheds-in-springfield-ohio/
/locations/storage-buildings-in-cincinnati-ohio/
/locations/sheds-in-dublin-ohio/
/locations/storage-buildings-in-kettering-ohio/
/locations/backyard-sheds-in-huber-heights-ohio/
/locations/storage-buildings-in-beaver-creek-ohio/
/locations/storage-buildings-in-lancaster-ohio/
/locations/storage-buildings-in-newark-ohio/
/locations/sheds-for-sale-westerville-ohio/
/locations/sheds-for-sale-in-worthington-oh/
/locations/sheds-for-sale-in-grove-city-oh/
/locations/sheds-for-sale-in-blacklick-estates-ohio/
/locations/storage-buildings-delaware/
/locations/sheds-in-indian-lake-ohio/
/locations/prefab-buildings-in-marysville-ohio/
/locations/storage-buildings-in-vandalia-ohio/
/locations/sheds-for-sale-in-whitehall-oh/
/locations/sheds-for-sale-in-gahanna-ohio/
/locations/sheds-for-sale-in-urbana-ohio/
/locations/sheds-for-sale-in-lincoln-village-oh/
/locations/sheds-in-new-albany-ohio/
/locations/sheds-for-sale-in-upper-arlington-ohio/
```

**For EACH location page verify:**
- [ ] Page is NOT blank (substantial local content beyond header/footer)
- [ ] Correct city name in title, H1, and body
- [ ] Content is unique (not exact copy of another location page)
- [ ] Shed styles listed (Gable, Quaker, Cape Cod, Classic, etc.)
- [ ] On-site build availability mentioned
- [ ] Delivery information for this area
- [ ] Rent-to-own mention
- [ ] Photos present and loading
- [ ] CTA to get a quote or use 3D Builder
- [ ] Garage options mentioned
- [ ] Custom shed option mentioned
- [ ] No wrong city name (copy-paste error)
- [ ] No PHP errors
- [ ] All internal links work

**Likely additional location pages (the automated crawler will discover all):**
These Ohio cities probably have dedicated pages - check if they exist on staging:
Hilliard, Pataskala, Pickerington, Reynoldsburg, London, Upper Arlington, Powell, Xenia, Troy, Piqua, Sidney, Washington Court House, Circleville, Mount Vernon, Marion, Findlay, Ashland, Mansfield, Wooster, Mount Gilead, Granville, Sunbury, Canal Winchester, Groveport, Obetz, Whitehall, Bexley, Galloway, West Jefferson, Mechanicsburg, New Carlisle, Enon, Yellow Springs, Cedarville, Jamestown, Wilmington, Greenville, Eaton, Miamisburg, Centerville, Bellefontaine, Kenton, Lima, Wapakoneta, Tipp City, and more.

---

### F. BLOG / TIPS & STORIES PAGES (26+ pages)

**Check each page is NOT blank and has real article content:**

```
/tips-stories/                                          (blog index)
/tips-stories/the-home-farm/
/tips-stories/this-old-barn/
/tips-stories/deciding-what-size-shed-you-need/
/tips-stories/8-x-10-storage-shed-pros-and-cons/
/tips-stories/10x12-sheds/
/tips-stories/shed-permits-in-ohio/
/tips-stories/garden-shed-insulation-spray-foam/
/tips-stories/best-shed-foundations/
/tips-stories/outdoor-kitchen-shed-ultimate-guide/
/tips-stories/10-superman-cave-shed-ideas/
/tips-stories/12-shed-bar-ideas-2021/
/tips-stories/a-porch-trait-of-sheds/
/tips-stories/she-sheds/
/tips-stories/a-hangout-shed-for-a-backyard-vacation-spot/
/tips-stories/home-office-sheds/
/tips-stories/quick-guide-to-an-affordable-gym-shed/
/tips-stories/shed-interior-ideas/
/tips-stories/how-to-top-off-your-new-shed/
/tips-stories/floored/
/tips-stories/kitschen-bakery-farm-stand-shed/
/tips-stories/jefferson-street-oasis-customer-story/
/tips-stories/prefab-pool-house-ideas/
/tips-stories/prefab-cabin-getaway/
/tips-stories/vinyl-siding-for-storage-shed/
/10x10-sheds-everything-you-need-to-know/              (root-level)
/8-x-10-storage-shed-pros-and-cons/                    (root-level)
/10-superman-cave-shed-ideas/                          (root-level, alt URL)
```

**For each blog post verify:**
- [ ] Article content loads (not blank)
- [ ] Featured image displays
- [ ] Text is well-formatted (headings, paragraphs, lists)
- [ ] Internal links work
- [ ] Images within article load
- [ ] Author/date info present
- [ ] No PHP errors
- [ ] No placeholder text

---

### G. INVENTORY ITEM PAGES (18+ confirmed)

**Spot-check several inventory items:**
```
/inventory/10x20-cabin-15945/
/inventory/8x12-cabin-15143/
/inventory/8x12-cape-cod-15372/
/inventory/8x12-mini-barn-15375/
/inventory/10x20-cottage-2-14923/
/inventory/8x8-mini-barn-13086/
/inventory/10x16-quaker-15411/
/inventory/10x20-modern-studio-14947/
/inventory/8x10-mini-barn-15009/
/inventory/10x12-modern-studio-16174/
/inventory/12x16-cottage-15882/
/inventory/10x12-cape-cod-16273/
/inventory/14x24-gable-16262/
/inventory/12x24-gable-garage-16319/
/inventory/12x20-cape-cod-3-16302/
/inventory/14x28-gable-garage-16259/
/inventory/12x20-cape-cod-2-16300/
/inventory/1014-gable-16704/
/inventory/10x16-gable-3-16310/
```

**For each inventory item:**
- [ ] Product photos load
- [ ] Size, style, stock number displayed
- [ ] Price shown (with sale price if applicable)
- [ ] Clearance/sale badges display
- [ ] Specifications listed
- [ ] CTA to inquire/purchase
- [ ] NOT blank page
- [ ] Inventory items on staging match production

---

### H. Legacy / Redirect URLs (Verify these redirect properly)

These old-format URLs exist on the production site. Verify they redirect correctly on staging:

```
/highwall-shed.php                    -> should redirect to /storage-sheds/highwall/
/10-superman-cave-shed-ideas/         -> may redirect to /tips-stories/10-superman-cave-shed-ideas/
/8-x-10-storage-shed-pros-and-cons/   -> may redirect to /tips-stories/8-x-10-storage-shed-pros-and-cons/
/shedsize8x12/                        -> may redirect to /shed-sizes/8x12-sheds/ (or standalone page)
/shedsize10x16/                       -> may redirect to /shed-sizes/10x16-sheds/ (or standalone page)
/shedsize10x20/                       -> may redirect to /shed-sizes/10x20-sheds/ (or standalone page)
/shedsize12x16/                       -> may redirect to /shed-sizes/12x16-sheds-in-ohio/ (or standalone page)
/shedsize12x28/                       -> may redirect to /shed-sizes/12x28-sheds/ (or standalone page)
```

**For each legacy URL:**
- [ ] URL returns 301 redirect or loads content (NOT 404)
- [ ] If redirect, destination page loads correctly
- [ ] No redirect loops
- [ ] If standalone page, content matches the corresponding /shed-sizes/ page

---

## Global Checks (Apply to ALL 269+ Pages)

### Navigation
- [ ] Main menu consistent across all pages
- [ ] All menu dropdowns work (desktop)
- [ ] Mobile hamburger menu opens/closes
- [ ] Logo links to homepage
- [ ] No broken menu links
- [ ] Menu includes: Storage Sheds, Garages, Shed Sizes, Inventory, Rent-to-Own, On-Site Build, More...

### Footer
- [ ] Present on all pages
- [ ] 8720 Amish Pike, Plain City, OH 43064
- [ ] (614) 873-4193
- [ ] Mon-Fri 8AM-5PM, Sat 10AM-2PM
- [ ] Social media links work
- [ ] Footer nav links work
- [ ] Copyright year: 2026

### Mobile Responsiveness
- [ ] No horizontal scroll at any width
- [ ] Readable text without zoom
- [ ] Tap targets >= 44px
- [ ] Images scale properly
- [ ] Forms usable on mobile

### Performance
- [ ] Pages load < 5 seconds
- [ ] No oversized images (>500KB each)
- [ ] No unnecessary redirects

### SEO
- [ ] Every page has unique `<title>`
- [ ] Every page has meta description
- [ ] Staging has `noindex` to prevent indexing
- [ ] All images have alt text
- [ ] No broken canonical URLs

### WordPress Migration
- [ ] No hardcoded `www.beachybarns.com` URLs in content
- [ ] No hardcoded `www.beachybarns.com` URLs in images
- [ ] All internal links point to staging domain
- [ ] Forms submit to staging domain (not production)
- [ ] 3D Shed Builder tool works on staging
- [ ] Request a Quote form submits correctly

---

## Priority Issues to Watch For

1. **BLANK PAGES** - Pages with only header + footer, no body content. Most common with page builders (Elementor/WPBakery) that weren't migrated properly.

2. **404 ERRORS** - Pages on production that return "Not Found" on staging. Indicates incomplete content migration.

3. **HARDCODED PRODUCTION URLS** - Links and images pointing to `www.beachybarns.com` instead of the staging domain. WordPress hardcodes URLs in the database - a search-replace is needed.

4. **BROKEN IMAGES** - Production image paths that don't resolve on staging. Check both media library images and CSS background images.

5. **PHP/DATABASE ERRORS** - Visible "Fatal error", "Warning", "Notice", or "Error establishing a database connection" messages.

6. **MISSING PLUGINS** - If page builder plugins (Elementor, WPBakery, Divi) or form plugins (Gravity Forms, WPForms, Contact Form 7) weren't migrated, those pages will appear broken or blank.

7. **3D BUILDER INTEGRATION** - The 3D Shed Builder is referenced across many pages. Verify it loads and works on the staging domain.

8. **INVENTORY SYNC** - Inventory items may differ between production and staging if the staging database is from an older snapshot.

---

*Report generated: 2026-02-06 (Updated)*
*190+ pages confirmed via search index*
*Run the automated crawler (`python src/staging_qa_report.py`) locally to discover all 269+ pages*
