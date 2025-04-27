---
authors: {{authors}}
aliases: {{aliases}}
tags: 
category:
year_created:
year_published: {{year}}
date_started:
date_finished: 
pages_total: {{pages}}
pages_read: 
downloaded: false
calibre: false
onyx boox: false
quotes: false
processed: false
on_the_table: false
cover_name: {{image_name}}
cssclasses:
  - book-page
---

```dataviewjs
let cover_path = '../_covers/' + dv.current().cover_name
dv.el('div', '<div class="book-cover"><img src="' + cover_path +'" /></div>');
```

```dataviewjs
dv.el('div', '<div class="break-block"></div>');
```

>[!tip] Slogan
> {{slogan}}

--- 


>[!info] Links
> {{book_page_url}}
>
