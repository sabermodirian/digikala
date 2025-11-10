// static/js/cart.js - FINAL VERSION

document.addEventListener('DOMContentLoaded', function () {
    // === عناصر DOM ===
    const cartIconLink = document.querySelector('a[href="/cart"]');
    const sideCart = document.getElementById('side-cart');
    const overlay = document.getElementById('side-cart-overlay');
    const closeCartBtn = document.getElementById('close-cart-btn');
    const cartBody = document.getElementById('side-cart-body');
    const emptyCartMessage = document.getElementById('empty-cart-message');
    const cartTotalPriceEl = document.getElementById('cart-total-price');
    const cartBadge = document.getElementById('cart-badge');

    // === توابع هسته سبد خرید ===
    const getCart = () => JSON.parse(localStorage.getItem('cart') || '[]');
    const saveCart = (cart) => {
        localStorage.setItem('cart', JSON.stringify(cart));
        renderCart(); // هر تغییری در سبد باید نمایش را بروز کند
    };

    // === توابع UI ===
    const openCart = () => {
        renderCart();
        sideCart.classList.add('active');
        overlay.classList.add('active');
    };
    const closeCart = () => {
        sideCart.classList.remove('active');
        overlay.classList.remove('active');
    };

    // === تابع اصلی رندر ===
    const renderCart = () => {
        const cart = getCart();
        cartBody.innerHTML = ''; 

        if (cart.length === 0) {
            if(emptyCartMessage) {
                cartBody.appendChild(emptyCartMessage);
                emptyCartMessage.style.display = 'block';
            }
        } else {
            if(emptyCartMessage) emptyCartMessage.style.display = 'none';
            cart.forEach(item => {
                const priceToShow = item.discounted_price > 0 ? item.discounted_price : item.price;
                const itemEl = document.createElement('div');
                itemEl.className = 'cart-item';
                itemEl.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <span class="cart-item-name">${item.name}</span>
                        <span class="cart-item-price">${(priceToShow * item.quantity).toLocaleString('fa-IR')} تومان</span>
                        <div class="cart-item-actions">
                            <button class="remove-item-btn" data-id="${item.seller_id}"><i class="fas fa-trash-alt"></i></button>
                            <div class="quantity-control">
                                <button class="quantity-btn" data-action="decrease" data-id="${item.seller_id}">-</button>
                                <span class="item-quantity">${item.quantity}</span>
                                <button class="quantity-btn" data-action="increase" data-id="${item.seller_id}">+</button>
                            </div>
                        </div>
                    </div>
                `;
                cartBody.appendChild(itemEl);
            });
        }
        updateCartBadge(cart);
        updateCartTotal(cart);
    };
    
    const updateCartBadge = (cart) => {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        if (cartBadge) {
            cartBadge.style.display = totalItems > 0 ? 'block' : 'none';
            cartBadge.innerText = totalItems;
        }
    };
    
    const updateCartTotal = (cart) => {
        const total = cart.reduce((sum, item) => {
            const price = item.discounted_price > 0 ? item.discounted_price : item.price;
            return sum + (price * item.quantity);
        }, 0);
        if (cartTotalPriceEl) {
            cartTotalPriceEl.innerText = `${total.toLocaleString('fa-IR')} تومان`;
        }
    };

    // === توابع مدیریت رویداد ===
    const handleAddToCart = (e) => {
        const button = e.target.closest('.add-to-cart-btn');
        if (!button) return;

        const cart = getCart();
        const { productId, sellerId, name, image, price, discountedPrice } = button.dataset;
        
        const existingItem = cart.find(item => item.seller_id === sellerId);

        if (existingItem) {
            existingItem.quantity++;
        } else {
            cart.push({
                product_id: parseInt(productId),
                seller_id: parseInt(sellerId),
                name,
                image,
                price: parseFloat(price),
                discounted_price: parseFloat(discountedPrice),
                quantity: 1,
            });
        }
        saveCart(cart);
        openCart(); // باز کردن سبد خرید پس از افزودن
    };

    const handleSideCartActions = (e) => {
        const button = e.target.closest('button[data-id]');
        if (!button) return;

        const sellerId = parseInt(button.dataset.id);
        const action = button.dataset.action || 'remove';
        let cart = getCart();
        const itemIndex = cart.findIndex(item => item.seller_id === sellerId);

        if (itemIndex === -1) return;

        if (action === 'increase') {
            cart[itemIndex].quantity++;
        } else if (action === 'decrease') {
            cart[itemIndex].quantity > 1 ? cart[itemIndex].quantity-- : cart.splice(itemIndex, 1);
        } else if (action === 'remove' || button.classList.contains('remove-item-btn')) {
            cart.splice(itemIndex, 1);
        }
        
        saveCart(cart);
    };

    // === ثبت Event Listeners ===
    if(cartIconLink) cartIconLink.addEventListener('click', (e) => { e.preventDefault(); openCart(); });
    if(closeCartBtn) closeCartBtn.addEventListener('click', closeCart);
    if(overlay) overlay.addEventListener('click', closeCart);
    if(cartBody) cartBody.addEventListener('click', handleSideCartActions);
    document.body.addEventListener('click', handleAddToCart);

    // === اجرای اولیه ===
    renderCart();
});
