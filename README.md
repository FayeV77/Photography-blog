# Kế hoạch triển khai website Learn Cine

## 1. Mục tiêu dự án

Xây dựng website blog có trải nghiệm và bố cục bám sát trang tham khảo:

- <https://www.thephotographyinstitute.com/us/en/blog>

Đặc trưng giao diện cần tái hiện:

- Nền website tối, có một ảnh nền lớn nằm ở lớp phía sau nội dung.
- Lớp phủ tối giúp chữ và các bài viết nổi rõ trên ảnh nền.
- Danh sách bài viết nằm phía trước theo dạng grid.
- Mỗi bài viết là một card gồm ảnh đại diện và tiêu đề.
- Card có nền tối, bo góc và tách khỏi lớp ảnh nền.
- Nhấn vào ảnh hoặc tiêu đề để mở trang chi tiết.
- Trang chi tiết hỗ trợ nội dung đan xen tự do giữa tiêu đề, văn bản và ảnh.
- Người quản trị đăng bài bằng giao diện soạn thảo, không cần sửa code.
- Website được build bằng Python và deploy miễn phí trên GitHub Pages.

Mục tiêu là tái tạo sát bố cục, tỷ lệ, màu sắc và hành vi responsive của trang tham khảo. Logo, nội dung, hình ảnh và các tài sản có bản quyền của website tham khảo không được sao chép; dự án sử dụng thương hiệu và hình ảnh riêng.

## 2. Phạm vi MVP

Phiên bản đầu tiên bao gồm:

- Trang danh sách bài viết.
- Trang chi tiết bài viết.
- Grid bài viết responsive.
- Ảnh nền cố định hoặc phủ toàn vùng nội dung.
- Ảnh cover cho từng bài.
- Nội dung rich text có ảnh xen kẽ.
- Chuyên mục và thẻ bài viết.
- Phân trang.
- Pages CMS để tạo, sửa, xóa và xuất bản bài.
- Chỉ một tài khoản quản trị duy nhất được phép truy cập CMS và thay đổi nội dung.
- Tối ưu ảnh bằng Python.
- SEO cơ bản, sitemap và RSS.
- Tự động build và deploy bằng GitHub Actions.
- Hosting trên GitHub Pages.

Chưa thực hiện trong MVP:

- Tài khoản độc giả.
- Bình luận do hệ thống tự quản lý.
- Thanh toán.
- Admin backend viết bằng FastAPI.
- Database PostgreSQL.
- Phân quyền biên tập nhiều cấp.
- Thống kê nâng cao do hệ thống tự lưu.

## 3. Kiến trúc được chọn

### 3.1 Công nghệ

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Core | Python 3.12 | Build website, kiểm tra nội dung, xử lý ảnh |
| Static Site Generator | Pelican | Chuyển Markdown thành HTML tĩnh |
| Template | Jinja2 | Xây dựng layout và component giao diện |
| Frontend | HTML5, CSS3, JavaScript thuần | Hiển thị và tương tác phía trình duyệt |
| CMS | Pages CMS | Giao diện viết bài và upload ảnh |
| Nội dung | Markdown + YAML front matter | Lưu bài viết trong GitHub |
| CI/CD | GitHub Actions | Test, build và deploy tự động |
| Hosting | GitHub Pages | Phục vụ website tĩnh miễn phí |

Không sử dụng React/Vue trong MVP vì nội dung chính là blog tĩnh. Cách này giảm JavaScript, tăng tốc độ tải và đơn giản hóa bảo trì.

### 3.2 Luồng xuất bản

```text
Người viết
    │
    ▼
Pages CMS (trình soạn thảo trực quan)
    │ lưu Markdown và ảnh
    ▼
GitHub repository
    │ kích hoạt workflow
    ▼
GitHub Actions
    ├── kiểm tra metadata
    ├── kiểm tra liên kết
    ├── tối ưu ảnh bằng Python
    ├── build Pelican/Jinja2
    └── upload artifact
    ▼
GitHub Pages
```

GitHub Pages chỉ phục vụ file tĩnh. Python chạy trong máy phát triển và GitHub Actions khi build; không có Python server chạy thường trực trên GitHub Pages.

## 4. Đặc tả giao diện frontend

### 4.1 Nguyên tắc visual

Các giá trị ban đầu được lấy theo tinh thần và cấu trúc quan sát được từ trang tham khảo, sau đó sẽ tinh chỉnh bằng đối chiếu screenshot:

```css
:root {
  --color-bg: #0c0c0c;
  --color-surface: #222222;
  --color-text: #ededed;
  --color-muted: #999999;
  --color-accent: #c7b88e;
  --card-radius: 10px;
  --content-max-width: 1140px;
  --grid-gap: 24px;
}
```

- Font chính: ưu tiên `Open Sans`; có system font fallback.
- Nội dung nằm trong container tối đa khoảng `1140px` trên desktop.
- Nền chính gần đen.
- Màu chữ sáng và màu nhấn vàng-be.
- Card bài viết có nền `#222`, padding khoảng `20px`, bo góc khoảng `10px`.
- Ảnh cover có bo góc nhẹ và tỷ lệ thống nhất.
- Tiêu đề card căn giữa, cỡ khoảng `18px` trên desktop.

### 4.2 Lớp ảnh nền

Ảnh nền là một asset riêng do chủ website cung cấp, ví dụ:

```text
theme/static/images/site-background.webp
```

Cấu trúc hiển thị:

```text
body
├── background image
├── dark overlay
└── page content
    ├── header
    ├── intro/hero
    ├── article grid
    └── footer
```

Yêu cầu:

- Ảnh nền dùng `cover` và đặt giữa theo chiều ngang.
- Lớp phủ tối có opacity dự kiến từ `0.55` đến `0.75`.
- Background không làm giảm độ tương phản của chữ.
- Trên màn hình nhỏ có thể tắt ảnh nền hoặc tăng overlay để tăng hiệu năng và khả năng đọc.
- Card bài viết phải nằm trên background bằng stacking context rõ ràng, không dùng giá trị `z-index` tùy tiện.
- Không tải ảnh nền quá lớn; mục tiêu dưới `350 KB` sau tối ưu.

### 4.3 Header

- Logo riêng của website.
- Menu desktop đặt ngang.
- Menu mobile dạng nút hamburger.
- Header trong suốt hoặc nền tối bán trong suốt.
- Các mục MVP: Trang chủ, Bài viết, Giới thiệu, Liên hệ.
- Trạng thái hover/focus sử dụng màu accent.
- Có vùng focus rõ ràng cho người dùng bàn phím.

### 4.4 Hero/intro của blog

- Tiêu đề lớn, ví dụ `Learn Cine Blog` hoặc tên blog thực tế.
- Dòng mô tả ngắn đặt bên dưới.
- Căn giữa tương tự trang tham khảo.
- Khoảng trắng dọc đủ lớn để tách header với grid.

Tên, tagline và nội dung thực tế sẽ được cấu hình trong file dữ liệu website, không hard-code trong template.

### 4.5 Grid bài viết

Breakpoint mục tiêu:

| Màn hình | Số cột | Ghi chú |
|---|---:|---|
| Từ 992px | 3 | Desktop |
| 576px–991px | 2 | Tablet |
| Dưới 576px | 1 | Mobile |

Mỗi `article-card` gồm:

- Link bao quanh ảnh và tiêu đề.
- Ảnh cover.
- Tiêu đề bài viết.
- Có thể bổ sung ngày/chuyên mục nhưng mặc định ẩn nếu làm giao diện lệch trang mẫu.
- Chiều cao card trong cùng một hàng phải cân đối.
- Ảnh có cùng aspect ratio, dự kiến `16:9` hoặc theo tỷ lệ xác nhận từ screenshot.
- Dùng `object-fit: cover` để tránh méo ảnh.
- Hover nhẹ: ảnh phóng tối đa khoảng `1.02`, card sáng hơn một mức hoặc có viền accent.
- Tôn trọng `prefers-reduced-motion`.

Không đặt chiều cao cố định cho tiêu đề. Dùng line clamp hợp lý trên trang danh sách nhưng vẫn phải cung cấp đầy đủ tiêu đề cho screen reader và trang chi tiết.

### 4.6 Phân trang

- Mỗi trang dự kiến 9 hoặc 12 bài để grid luôn cân đối.
- Nút Trang trước, số trang và Trang sau.
- Trạng thái trang hiện tại rõ ràng.
- URL tĩnh dạng `/blog/page/2/`.
- Phân trang hoạt động không cần JavaScript.

### 4.7 Trang chi tiết bài viết

URL dự kiến:

```text
/blog/<slug>/
```

Bố cục:

- Breadcrumb.
- Tiêu đề H1 duy nhất.
- Ngày đăng, tác giả và chuyên mục.
- Ảnh cover.
- Vùng nội dung có chiều rộng đọc khoảng `720–800px`.
- Bài liên quan ở cuối trang.
- Điều hướng bài trước/bài sau.

Nội dung cho phép thứ tự tự do:

```text
Tiêu đề cấp 2
Văn bản
Ảnh
Ảnh
Văn bản
Tiêu đề cấp 2
Ảnh
Trích dẫn
Văn bản
```

Các element cần được style:

- `h2`, `h3`, `h4`.
- Đoạn văn.
- Chữ đậm, nghiêng.
- Danh sách có thứ tự và không thứ tự.
- Link.
- Blockquote.
- Ảnh đơn.
- Nhiều ảnh liên tiếp.
- Chú thích ảnh.
- Đường phân cách.
- Code block nếu có.

Ảnh trong nội dung:

- Không vượt chiều rộng vùng bài viết.
- Giữ đúng tỷ lệ.
- Có `alt` bắt buộc.
- Lazy load, trừ ảnh đầu trang.
- Có thể bấm để mở lightbox ở giai đoạn hoàn thiện.
- Hai ảnh liên tiếp mặc định vẫn xếp dọc; gallery hai cột là tính năng mở rộng.

### 4.8 Footer

- Menu phụ.
- Copyright.
- Liên kết chính sách nếu có.
- Màu chữ muted.
- Không sao chép nội dung hoặc thương hiệu của trang tham khảo.

## 5. CMS và quy trình đăng bài không cần code

### 5.1 Pages CMS

Pages CMS được cấu hình bằng file `.pages.yml` một lần bởi lập trình viên. Sau đó người viết thao tác trên giao diện web.

Các trường của bài viết:

| Trường | Kiểu | Bắt buộc | Ghi chú |
|---|---|---:|---|
| `title` | Text | Có | Tiêu đề bài |
| `slug` | Text | Có | Chỉ chữ thường, số và dấu gạch ngang |
| `date` | Date/time | Có | Ngày xuất bản |
| `author` | Text/select | Có | Tác giả |
| `category` | Select | Có | Một chuyên mục chính |
| `tags` | List | Không | Nhiều thẻ |
| `summary` | Textarea | Có | Mô tả cho card và SEO |
| `cover` | Image | Có | Ảnh trên grid và đầu bài |
| `cover_alt` | Text | Có | Mô tả ảnh cover |
| `published` | Boolean | Có | Nháp hoặc xuất bản |
| `body` | Rich text | Có | Nội dung đan xen chữ và ảnh |
| `seo_title` | Text | Không | Mặc định lấy `title` |
| `seo_description` | Textarea | Không | Mặc định lấy `summary` |

Trình soạn thảo rich text phải cho phép:

- Chọn Heading 2, Heading 3.
- In đậm, in nghiêng.
- Chèn link.
- Danh sách.
- Trích dẫn.
- Upload và chèn ảnh tại vị trí con trỏ.
- Chèn nhiều ảnh liên tiếp.
- Chuyển giữa giao diện trực quan và Markdown khi cần.

### 5.2 Chính sách một tài khoản admin duy nhất

Hệ thống chỉ có **một tài khoản admin**. Không có chức năng đăng ký, mời thành viên, tạo thêm người dùng hoặc phân quyền nhiều cấp.

Tài khoản admin sử dụng chính tài khoản GitHub của chủ website để đăng nhập Pages CMS. GitHub là nơi xác thực danh tính và quản lý mật khẩu/2FA; website không tự lưu mật khẩu. Tài khoản này là tài khoản duy nhất có quyền ghi vào repository và được phép:

- Tạo bài viết.
- Sửa bài viết.
- Xóa bài viết.
- Upload hoặc xóa ảnh.
- Lưu bản nháp.
- Xuất bản hoặc gỡ bài.
- Kích hoạt quá trình build/deploy thông qua commit nội dung.

Mọi tài khoản khác chỉ có thể xem website công khai, không thể truy cập chức năng quản trị hoặc thay đổi repository. Không hiển thị nút tạo tài khoản và không triển khai API đăng ký người dùng.

Thông tin định danh không nhạy cảm của admin được lưu tại `data/admin.yml`:

```yaml
schema_version: 1
single_admin: true
admin:
  github_username: "REPLACE_WITH_GITHUB_USERNAME"
  display_name: "Website Administrator"
  role: "admin"
  active: true
  permissions:
    - create_post
    - edit_post
    - delete_post
    - publish_post
    - manage_media
```

`REPLACE_WITH_GITHUB_USERNAME` phải được thay bằng GitHub username thật của chủ website trước khi triển khai. Metadata này dùng để khai báo chủ sở hữu và kiểm tra cấu hình; quyền bảo mật thực tế phải được cưỡng chế bằng GitHub repository permissions và quyền cài đặt Pages CMS GitHub App.

Các nguyên tắc bắt buộc:

- Chỉ GitHub username khai báo trong `data/admin.yml` được có quyền `write`, `maintain` hoặc `admin` đối với repository.
- Không thêm collaborator khác có quyền ghi.
- Bật xác thực hai lớp (2FA) cho tài khoản GitHub admin.
- Không lưu mật khẩu, GitHub personal access token, OAuth token, private key hoặc recovery code trong metadata hay repository.
- Secret phục vụ CI/CD hoặc OAuth, nếu phát sinh, chỉ được lưu trong GitHub Actions Secrets hoặc secret store của nhà cung cấp xác thực.
- Script validation phải báo lỗi nếu metadata chứa nhiều hơn một admin, admin không hoạt động hoặc còn giá trị placeholder.
- Nếu cần đổi admin, phải thay GitHub repository permission và `data/admin.yml` trong cùng một quy trình bàn giao; không tồn tại đồng thời hai admin.

Việc “tạo sẵn tài khoản” trong dự án có nghĩa là tạo sẵn hồ sơ `data/admin.yml` và cấu hình quyền cho một GitHub account đã tồn tại. Dự án không thể và không nên tự tạo mật khẩu hoặc tài khoản GitHub giả trong source code. Sau khi chủ website cung cấp GitHub username, giá trị placeholder sẽ được thay và tài khoản đó trở thành admin duy nhất.

### 5.3 Luồng làm việc của admin

1. Truy cập `https://app.pagescms.org/`.
2. Đăng nhập bằng đúng GitHub account được khai báo trong `data/admin.yml`.
3. Chọn repository website.
4. Chọn **Bài viết**.
5. Chọn **Tạo bài viết mới**.
6. Điền tiêu đề, ảnh cover và các metadata.
7. Viết nội dung, chèn ảnh tại vị trí mong muốn.
8. Để `published: false` nếu là bản nháp.
9. Xem preview nếu workflow preview đã được bật.
10. Chuyển sang xuất bản và lưu.
11. GitHub Actions tự build và deploy.

### 5.4 Định dạng lưu trữ

Ví dụ file do CMS tạo:

```markdown
---
title: "Hướng dẫn chụp ảnh chân dung"
slug: "huong-dan-chup-anh-chan-dung"
date: 2026-09-29 09:00
author: "Tên tác giả"
category: "Kỹ thuật"
tags:
  - portrait
  - lighting
summary: "Những nguyên tắc cơ bản để bắt đầu chụp chân dung."
cover: "/images/blog/portrait-cover.webp"
cover_alt: "Chân dung trong ánh sáng tự nhiên"
published: true
---

## Chuẩn bị thiết bị

Bạn cần lựa chọn ống kính phù hợp với điều kiện chụp.

![Máy ảnh và ống kính](/images/blog/camera-and-lens.webp)

![Thiết lập máy ảnh](/images/blog/camera-settings.webp)

Sau khi chuẩn bị thiết bị, hãy kiểm tra ánh sáng tại địa điểm chụp.

## Thiết lập ánh sáng

![Thiết lập ánh sáng chân dung](/images/blog/portrait-lighting.webp)
```

Pelican sử dụng plugin `pelican-yaml-metadata` để đọc YAML front matter này.

## 6. Xử lý ảnh

### 6.1 Quy tắc upload

- Định dạng cho phép: JPG, JPEG, PNG, WebP và AVIF nếu pipeline hỗ trợ ổn định.
- Không cho phép SVG upload tự do từ người viết để tránh nội dung không an toàn.
- Tên file được slugify, bỏ dấu và khoảng trắng.
- Kích thước file upload đề xuất không quá `10 MB`.
- Mỗi ảnh bắt buộc có alt text trong nội dung hoặc trường đi kèm.

### 6.2 Pipeline Python

Script `scripts/optimize_images.py` thực hiện:

- Đọc ảnh mới hoặc thay đổi.
- Sửa orientation từ EXIF.
- Loại metadata không cần thiết.
- Sinh bản cover/card theo kích thước mục tiêu.
- Sinh WebP tối ưu.
- Không upscale ảnh nhỏ.
- Giữ file nguồn theo cấu hình hoặc loại khỏi output production.

Kích thước dự kiến:

| Biến thể | Chiều rộng | Mục đích |
|---|---:|---|
| Thumbnail | 480px | Mobile/grid nhỏ |
| Card | 800px | Grid desktop |
| Content | 1280px | Ảnh trong bài |
| Large | 1920px | Lightbox nếu cần |

Template sử dụng `srcset` và `sizes` để trình duyệt tải đúng biến thể.

## 7. Cấu trúc thư mục dự kiến

```text
website/
├── .github/
│   └── workflows/
│       ├── deploy.yml
│       └── pull-request.yml
├── content/
│   ├── articles/
│   ├── pages/
│   └── images/
│       └── blog/
├── data/
│   ├── admin.yml
│   ├── authors.yml
│   ├── categories.yml
│   └── site.yml
├── scripts/
│   ├── optimize_images.py
│   ├── validate_content.py
│   └── check_internal_links.py
├── tests/
│   ├── test_content.py
│   └── test_build.py
├── theme/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── article.html
│   │   ├── article-card.html
│   │   ├── category.html
│   │   ├── pagination.html
│   │   └── 404.html
│   └── static/
│       ├── css/
│       │   ├── tokens.css
│       │   ├── base.css
│       │   ├── layout.css
│       │   ├── components.css
│       │   └── article.css
│       ├── js/
│       │   └── main.js
│       └── images/
│           └── site-background.webp
├── .pages.yml
├── pelicanconf.py
├── publishconf.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 8. Backend/build layer

### 8.1 Cấu hình Pelican

- Định dạng URL bài: `/blog/{slug}/`.
- Chỉ build bài có `published: true` cho production.
- Sắp xếp bài mới nhất trước.
- Tạo category, tag, pagination, archive và feed.
- Tách `pelicanconf.py` cho local và `publishconf.py` cho production.
- Thiết lập đúng `SITEURL` và relative URL cho GitHub project pages.
- Copy static assets có hash hoặc version để tránh cache cũ.

### 8.2 Validation

Build phải thất bại khi:

- Thiếu title, slug, date, summary, cover hoặc cover alt.
- Hai bài trùng slug.
- Slug chứa ký tự không hợp lệ.
- Ảnh cover không tồn tại.
- Link nội bộ trỏ đến trang không tồn tại.
- Bài đã publish nhưng ngày hoặc metadata sai định dạng.

Build chỉ cảnh báo khi:

- Ảnh quá lớn.
- Summary quá ngắn hoặc quá dài.
- Bài không có H2.
- Ảnh trong nội dung thiếu alt text.

## 9. SEO và chia sẻ mạng xã hội

Mỗi bài cần có:

- HTML title riêng.
- Meta description.
- Canonical URL.
- Open Graph title, description và image.
- Twitter/X card.
- JSON-LD `BlogPosting`.
- Một H1 duy nhất.
- Heading theo đúng thứ tự.
- URL không dấu và ổn định.

Website cần có:

- `sitemap.xml`.
- `robots.txt`.
- RSS/Atom feed.
- Trang 404 tùy chỉnh.
- Canonical domain chính xác.

## 10. Accessibility

- Contrast đạt WCAG AA.
- Tất cả ảnh nội dung có alt text hoặc alt rỗng nếu chỉ trang trí.
- Card có accessible name rõ ràng.
- Menu mobile điều khiển được bằng bàn phím.
- Focus không bị loại bỏ.
- Thứ tự heading hợp lý.
- Có link bỏ qua điều hướng `Skip to content`.
- Lightbox nếu có phải giữ focus và đóng được bằng Escape.
- Animation giảm hoặc tắt khi người dùng bật `prefers-reduced-motion`.

## 11. Hiệu năng

Mục tiêu production:

- Lighthouse Performance từ 90 trở lên trên mobile.
- Lighthouse Accessibility từ 90 trở lên.
- Lighthouse SEO từ 90 trở lên.
- Không có layout shift đáng kể do ảnh.
- CSS và JavaScript ban đầu nhỏ gọn.
- JavaScript không bắt buộc để đọc bài.
- Ảnh ngoài viewport dùng lazy loading.
- Ảnh hero/LCP được preload hoặc đặt priority phù hợp.
- Tổng dung lượng tải trang danh sách ban đầu mục tiêu dưới `1.5 MB`.

## 12. GitHub Actions và deploy

Workflow `deploy.yml` chạy khi push vào `main`:

1. Checkout repository.
2. Cài Python phiên bản cố định.
3. Cache pip.
4. Cài dependencies.
5. Validate nội dung.
6. Tối ưu ảnh.
7. Chạy test.
8. Build Pelican vào `output/`.
9. Kiểm tra link trong output.
10. Upload GitHub Pages artifact.
11. Deploy vào environment `github-pages`.

Workflow pull request:

- Build nhưng không deploy production.
- Chạy validation và test.
- Có thể tạo artifact preview để kiểm tra thủ công.

Thiết lập repository:

- GitHub Pages source: GitHub Actions.
- Branch production: `main`.
- Bật HTTPS.
- Không commit secret vào repository.
- Repository public nếu sử dụng GitHub Free theo mô hình đơn giản nhất.

## 13. Môi trường local

Yêu cầu:

- Python 3.12.
- Git.
- Trình duyệt hiện đại.

Các lệnh dự kiến sau khi dự án được scaffold:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
pelican --listen --autoreload
```

Trên máy Windows đang dùng Anaconda/Conda, có thể gọi Python trực tiếp từ environment hiện tại (ví dụ base) thay cho lệnh `python` nếu Python chưa có trong `PATH`:

```powershell
& 'D:\anaconda\python.exe' -m pip install -r requirements-dev.txt
& 'D:\anaconda\Scripts\pelican.exe' content -s pelicanconf.py -o output
```

Local demo dùng `--allow-placeholder-admin` khi `data/admin.yml` chưa có GitHub username thật. Không dùng cờ này cho production.

Kiểm tra trước khi commit:

```bash
python scripts/validate_content.py
python -m pytest
pelican content -s publishconf.py
```

## 14. Kế hoạch triển khai chi tiết

### Giai đoạn 0 — Xác nhận đầu vào

Thời gian: 0.5 ngày.

- Xác nhận tên website, logo và menu.
- Nhận ảnh nền riêng.
- Nhận bảng màu hoặc chấp nhận palette dự kiến.
- Xác nhận domain GitHub Pages.
- Chuẩn bị 5 bài viết và ảnh mẫu.
- Chụp screenshot trang tham khảo ở desktop, tablet và mobile làm baseline.

Kết quả: bộ asset và tiêu chí visual được chốt.

### Giai đoạn 1 — Nền tảng Python/Pelican

Thời gian: 1 ngày.

- Khởi tạo cấu trúc thư mục.
- Cấu hình Pelican, Markdown và YAML metadata.
- Định nghĩa URL.
- Tạo dữ liệu mẫu.
- Cấu hình draft/published.
- Thêm validation cơ bản.

Kết quả: build được trang HTML tĩnh từ bài Markdown.

### Giai đoạn 2 — Theme bám sát trang mẫu

Thời gian: 2–3 ngày.

- Tạo design tokens.
- Xây header và navigation.
- Xây ảnh nền và dark overlay.
- Xây hero blog.
- Xây grid 3/2/1 cột.
- Xây card ảnh và tiêu đề.
- Xây phân trang.
- Xây footer.
- Tinh chỉnh typography, spacing, radius và hover.

Kết quả: trang danh sách bám sát screenshot mục tiêu.

### Giai đoạn 3 — Trang bài viết

Thời gian: 1.5–2 ngày.

- Tạo layout chi tiết.
- Style toàn bộ rich-text element.
- Hỗ trợ ảnh xen kẽ nội dung.
- Thêm breadcrumb.
- Thêm bài liên quan và điều hướng trước/sau.
- Thêm lightbox nếu còn trong phạm vi MVP đã duyệt.

Kết quả: bài dài đọc tốt trên desktop và mobile.

### Giai đoạn 4 — Pages CMS

Thời gian: 1–1.5 ngày.

- Tạo `.pages.yml`.
- Tạo `data/admin.yml` với đúng một hồ sơ admin.
- Khai báo schema bài viết.
- Khai báo thư viện media.
- Cấu hình rich text.
- Thiết lập GitHub App và quyền repository.
- Chỉ cấp quyền ghi repository cho GitHub account của admin.
- Xác nhận không có chức năng đăng ký hoặc tạo thêm tài khoản.
- Kiểm thử tạo, sửa, xóa, nháp và xuất bản.
- Viết hướng dẫn sử dụng ngắn cho người biên tập.

Kết quả: người dùng đăng bài và chèn ảnh không cần code.

### Giai đoạn 5 — Ảnh, SEO và accessibility

Thời gian: 1.5 ngày.

- Tạo pipeline tối ưu ảnh.
- Thêm responsive image.
- Thêm sitemap, feed, Open Graph và JSON-LD.
- Kiểm tra heading, alt và keyboard navigation.
- Tối ưu font và critical assets.

Kết quả: website đạt yêu cầu SEO và hiệu năng cơ bản.

### Giai đoạn 6 — CI/CD và nghiệm thu

Thời gian: 1–1.5 ngày.

- Tạo GitHub Actions.
- Deploy GitHub Pages.
- Kiểm tra base URL.
- Kiểm tra link hỏng.
- Chạy Lighthouse.
- So sánh screenshot ở các viewport chuẩn.
- Sửa các sai lệch visual.
- Kiểm thử quy trình đăng bài thực tế.

Kết quả: website production và tài liệu bàn giao.

Tổng thời gian dự kiến: **8–11 ngày làm việc**, chưa tính thời gian chuẩn bị nội dung và vòng phản hồi thiết kế.

## 15. Tiêu chí nghiệm thu

### Giao diện

- Có ảnh nền phía sau và overlay đúng thiết kế.
- Card bài viết nổi rõ phía trên background.
- Desktop hiển thị 3 cột, tablet 2 cột, mobile 1 cột.
- Ảnh card không bị méo.
- Khoảng cách, typography, màu sắc và radius bám sát baseline screenshot.
- Không có thanh cuộn ngang ở viewport từ 320px trở lên.

### Nội dung/CMS

- Admin tạo bài mà không sửa code.
- Có thể chèn tiêu đề, chữ đậm, danh sách, link và ảnh.
- Có thể sắp xếp `text → ảnh → ảnh → text → heading → ảnh`.
- Upload ảnh thành công và ảnh xuất hiện đúng vị trí.
- Bài nháp không xuất hiện trên production.
- Bài xuất bản xuất hiện sau khi workflow hoàn tất.
- Chỉ GitHub account được khai báo trong `data/admin.yml` có thể tạo, sửa, xóa hoặc xuất bản bài.
- Không có chức năng đăng ký và không thể tạo tài khoản thứ hai từ website/CMS.
- Validation thất bại nếu cấu hình có nhiều hơn một admin hoặc vẫn còn username placeholder.

### Kỹ thuật

- Build production thành công từ repository sạch.
- Không có link nội bộ hỏng.
- Không có lỗi HTML nghiêm trọng.
- GitHub Actions tự deploy khi CMS lưu bài đã xuất bản.
- URL hoạt động đúng cả khi website nằm dưới project path.
- Trang vẫn đọc được khi JavaScript bị tắt.

### Chất lượng

- Lighthouse các mục Performance, Accessibility và SEO đạt từ 90 trở lên trong điều kiện đo thống nhất.
- Ảnh có kích thước khai báo để hạn chế layout shift.
- Không có secret hoặc token trong Git.
- Không có mật khẩu, recovery code hoặc thông tin xác thực của admin trong metadata.
- Nội dung và asset không sao chép từ website tham khảo.

## 16. Rủi ro và hướng xử lý

| Rủi ro | Ảnh hưởng | Hướng xử lý |
|---|---|---|
| GitHub Pages không chạy Python server | Không có API runtime | Python chỉ chạy lúc build; dùng dịch vụ riêng nếu cần API sau này |
| Ảnh upload quá lớn | Website chậm, repository phình to | Validation và pipeline resize/WebP |
| CMS commit làm build lỗi | Website mới không deploy | Validation trước deploy; bản đang chạy vẫn giữ nguyên |
| Sai base URL của project pages | Hỏng CSS/ảnh/link | Dùng helper URL của Pelican và test trên subpath |
| Muốn giống tuyệt đối nhưng thiếu screenshot/asset | Khó nghiệm thu visual | Chốt screenshot baseline và viewport trước khi code |
| GitHub account admin bị mất quyền truy cập | Không thể đăng bài hoặc quản trị repo | Bật 2FA, lưu recovery code ngoài repository và duy trì quy trình khôi phục của GitHub |
| Cấp nhầm quyền ghi cho tài khoản khác | Vi phạm chính sách single-admin | Audit repository collaborators và GitHub App permissions trước nghiệm thu |
| Sao chép tài sản của trang mẫu | Rủi ro bản quyền/thương hiệu | Chỉ tái tạo layout; dùng logo, ảnh và nội dung riêng |

## 17. Khả năng mở rộng sau MVP

- Tìm kiếm client-side bằng index JSON.
- Gallery hai hoặc ba cột trong rich text.
- Video YouTube/Vimeo.
- Newsletter qua dịch vụ bên thứ ba.
- Bình luận qua dịch vụ bên thứ ba.
- Preview deployment cho bản nháp.
- Đa ngôn ngữ.
- FastAPI và PostgreSQL khi cần dữ liệu động.
- Object storage/CDN nếu thư viện ảnh lớn.
- Admin riêng nếu Pages CMS không còn đáp ứng workflow biên tập.

## 18. Các đầu vào cần cung cấp trước khi bắt đầu

- Tên website.
- Logo bản sáng và bản tối, ưu tiên SVG.
- Ảnh nền chất lượng cao có quyền sử dụng.
- Màu thương hiệu nếu không dùng palette dự kiến.
- Danh sách menu.
- Tên GitHub account/organization và repository.
- GitHub username chính xác của tài khoản sẽ làm admin duy nhất.
- Email hiển thị của admin nếu muốn công khai tên tác giả; không dùng email này làm secret đăng nhập.
- Domain riêng nếu có.
- Danh sách tác giả và chuyên mục.
- Tối thiểu 5 bài viết mẫu.
- Ảnh cover và ảnh nội dung cho các bài mẫu.

## 19. Định nghĩa hoàn thành

Dự án được xem là hoàn thành khi:

- Toàn bộ tiêu chí nghiệm thu đã đạt.
- Website chạy trên GitHub Pages qua HTTPS.
- Có thể đăng một bài hoàn chỉnh từ Pages CMS mà không dùng code.
- Chỉ một GitHub account admin đã khai báo có thể tạo, sửa, xóa và xuất bản nội dung.
- Hồ sơ admin được lưu trong `data/admin.yml` nhưng không chứa mật khẩu, token hoặc secret.
- Bài hỗ trợ nội dung và ảnh đan xen đúng thứ tự.
- Workflow tự động build và deploy hoạt động ổn định.
- Người quản trị nhận được hướng dẫn đăng bài, sửa bài, tạo nháp và khôi phục phiên bản cũ.
- Source code, nội dung và cấu hình đều nằm trong repository thuộc quyền kiểm soát của chủ website.
