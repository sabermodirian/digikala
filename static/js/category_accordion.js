/* ===============================================================
   🚀 نسخه‌ی بهبود یافته آکاردیون با انیمیشن نرمی و سبک مدرن
   ===============================================================
   ✨ توضیح فارسی:
   تمام دسته‌هایی که زیرمنو دارند شناسایی می‌شوند، 
   آیکون فلش به آن‌ها اضافه می‌شود، و هنگام کلیک، 
   زیرمنو با افکت نرم و چرخش سینماتیک باز یا بسته می‌شود.

   ✨ English Explanation:
   A smooth, cinematic accordion effect for hierarchical
   category navigation; arrow rotation and soft fade-slide for submenu.
   =============================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.category-link');

    links.forEach(link => {
        const submenu = link.nextElementSibling;

        if (submenu && submenu.classList.contains('subcategory-list')) {
            link.classList.add('has-submenu');

            if (!link.querySelector('.dropdown-arrow')) {
                link.insertAdjacentHTML('beforeend', '<i class="bi bi-chevron-down dropdown-arrow"></i>');
            }

            link.addEventListener('click', event => {
                // 🚫 جلوگیری از رفتن به صفحه تا کاربر خودش یکی از زیرمنوها رو انتخاب کنه
                event.preventDefault();

                // باز/بسته کردن همین منو
                link.classList.toggle('open');
                submenu.classList.toggle('open');
            });
        }
    });

    // ✅ حفظ باز بودن منوی والد بر اساس URL صفحه فعلی
    const currentUrl = window.location.pathname;

    document.querySelectorAll('.subcategory-list a').forEach(subLink => {
        const href = subLink.getAttribute('href');
        if (href && currentUrl.includes(href)) {
            // فعال‌سازی آیتم فعلی
            subLink.classList.add('active');

            // باز نگه داشتن تمام منوهای والدش
            let parentMenu = subLink.closest('.subcategory-list');
            while (parentMenu) {
                parentMenu.classList.add('open');
                const parentLink = parentMenu.previousElementSibling;
                if (parentLink && parentLink.classList.contains('category-link')) {
                    parentLink.classList.add('open');
                }
                parentMenu = parentLink?.closest('.subcategory-list');
            }
        }
    });
});
