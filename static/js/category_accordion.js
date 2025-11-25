// static/js/category_accordion.js

document.addEventListener('DOMContentLoaded', function () {
    const categoryLinks = document.querySelectorAll('.category-link');

    categoryLinks.forEach(link => {
        const sublist = link.nextElementSibling;

        // اگر لینک یک لیست زیرمجموعه داشت (با کلاس .subcategory-list)
        if (sublist && sublist.classList.contains('subcategory-list')) {
            // ۱. اضافه کردن کلاس و آیکون فلش به لینک والد
            link.classList.add('has-submenu');
            // innerHTML برای افزودن آیکون بدون حذف متن فعلی
            link.innerHTML = `${link.textContent.trim()} <i class="bi bi-chevron-down dropdown-arrow"></i>`;

            // ۲. افزودن رویداد کلیک برای باز و بسته کردن
            link.addEventListener('click', function (event) {
                // جلوگیری از رفرش صفحه هنگام کلیک روی لینک والد
                event.preventDefault();

                // ۳. تغییر وضعیت کلاس‌ها برای نمایش/مخفی کردن زیرمنو و چرخش آیکون
                sublist.classList.toggle('open');
                link.classList.toggle('open');
            });
        }
    });
});
