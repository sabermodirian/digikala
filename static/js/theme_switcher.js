/**
 * کنترل‌کنندهٔ تم سایت (روشن/تاریک)
 * - دکمه: #themeToggle
 * - ذخیره‌سازی وضعیت در localStorage
 * - احترام به prefers-color-scheme سیستم در بارگذاری اولیه
 */

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('themeToggle');
    if (!toggleBtn) return; // اگر دکمه در DOM نبود، ادامه نده

    const bodyEl = document.body;
    const storageKey = 'fookala-theme';

    /**
     * آپدیت UI بر اساس تم انتخابی
     * @param {'light'|'dark'} theme
     */
    const applyTheme = (theme) => {
        bodyEl.dataset.theme = theme; // استایل‌ها از data-theme می‌خوانند
        localStorage.setItem(storageKey, theme);
        // به‌صورت دلخواه متن/ایموجی دکمه تغییر می‌کند
        toggleBtn.textContent = theme === 'dark' ? '🌞' : '🌙';
        toggleBtn.setAttribute('aria-label', theme === 'dark' ? 'تغییر به تم روشن' : 'تغییر به تم تاریک');
    };

    /**
     * تعیین تم اولیه
     * اولویت: ذخیرهٔ کاربر > تنظیمات سیستم > روشن
     */
    const savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === 'dark' || savedTheme === 'light') {
        applyTheme(savedTheme);
    } else {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark ? 'dark' : 'light');
    }

    /**
     * واکنش به کلیک دکمه
     */
    toggleBtn.addEventListener('click', () => {
        const nextTheme = bodyEl.dataset.theme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
    });
});
