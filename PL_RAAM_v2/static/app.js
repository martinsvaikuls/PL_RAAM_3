// ============================================================================
// RAAM Store - Frontend Application
// ============================================================================

const API_BASE = window.location.origin;
const DEBUG = false; // Set to true for development debugging

// ============================================================================
// PRODUCT DATA
// ============================================================================

const PRODUCTS = [
    { id: 1, name: "Classic Logo", design: "Classic Logo Design", baseColor: "white", price: 15, description: "Timeless design perfect for everyday wear", icon: "👔", category: "Classic" },
    { id: 2, name: "Mountain View", design: "Mountain Landscape", baseColor: "navy", price: 18, description: "Inspiring nature scene for adventure lovers", icon: "⛰️", category: "Nature" },
    { id: 3, name: "Abstract Art", design: "Abstract Geometric", baseColor: "black", price: 20, description: "Modern geometric patterns for the bold", icon: "🎨", category: "Art" },
    { id: 4, name: "Vintage Style", design: "Retro Vintage Print", baseColor: "gray", price: 17, description: "Nostalgic retro design with classic appeal", icon: "📻", category: "Vintage" },
    { id: 5, name: "Minimalist", design: "Simple Minimal Design", baseColor: "white", price: 16, description: "Clean and simple for the modern minimalist", icon: "✨", category: "Minimal" },
    { id: 6, name: "Bold Typography", design: "Bold Text Design", baseColor: "red", price: 19, description: "Make a statement with powerful typography", icon: "💪", category: "Bold" },
    { id: 7, name: "Ocean Waves", design: "Calming Ocean Scene", baseColor: "blue", price: 18, description: "Serene ocean waves for beach vibes", icon: "🌊", category: "Nature" },
    { id: 8, name: "City Lights", design: "Urban Nightscape", baseColor: "dark", price: 21, description: "Vibrant city lights for urban enthusiasts", icon: "🌃", category: "Urban" },
    { id: 9, name: "Floral Print", design: "Elegant Floral Pattern", baseColor: "pink", price: 17, description: "Beautiful floral patterns for spring", icon: "🌸", category: "Nature" }
];

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

let cart = JSON.parse(localStorage.getItem('cart') || '[]');

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function getAuthToken() {
    return localStorage.getItem('token');
}

function getUserInfo() {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
}

function saveUserSession(token, userInfo) {
    localStorage.setItem('token', token);
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
}

function clearUserSession() {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
}

// ============================================================================
// UI UTILITIES
// ============================================================================

function showMessage(text, type = 'success') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;
    setTimeout(() => {
        messageEl.className = 'message';
    }, 5000);
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function logError(context, error) {
    if (DEBUG) {
        console.error(`[${context}]`, error);
    }
}

// ============================================================================
// PAGE NAVIGATION
// ============================================================================

function showLogin() {
    hideAllSections();
    document.getElementById('login-section').style.display = 'block';
}

function showRegister() {
    hideAllSections();
    document.getElementById('register-section').style.display = 'block';
}

function showStore(user) {
    hideAllSections();
    document.getElementById('store-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'flex';
    document.getElementById('user-name').textContent = `Welcome, ${user.client_name}!`;
    
    // Show loading briefly for smooth transition
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block';
    
    setTimeout(() => {
        spinner.style.display = 'none';
        renderProducts();
        renderCart();
    }, 500);
}

function showCheckoutPage() {
    hideAllSections();
    document.getElementById('checkout-section').style.display = 'block';
    renderCheckoutItems();
}

function goBackToStore() {
    const user = getUserInfo();
    if (user) {
        showStore(user);
    }
}

function hideAllSections() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('store-section').style.display = 'none';
    document.getElementById('checkout-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
}

// ============================================================================
// PRODUCT DISPLAY
// ============================================================================

function getTextColorForBackground(color) {
    const lightColors = ['white', 'pink', 'gray'];
    return lightColors.includes(color.toLowerCase()) ? '#333' : 'white';
}

function renderProducts() {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = PRODUCTS.map(product => {
        const textColor = getTextColorForBackground(product.baseColor);
        return `
        <div class="product-card" data-category="${product.category}">
            <div class="product-badge">${product.category}</div>
            <div class="product-image" style="background: linear-gradient(135deg, var(--color-${product.baseColor}), var(--color-${product.baseColor}-dark))">
                <div class="product-icon">${product.icon || product.name.charAt(0)}</div>
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="product-design">${product.design}</p>
                <p class="product-description">${product.description}</p>
                <div class="product-meta">
                    <span class="product-color-badge" style="background-color: var(--color-${product.baseColor}); color: ${textColor}; border: 1px solid ${textColor === '#333' ? '#ddd' : 'transparent'}">${product.baseColor}</span>
                    <span class="product-price">$${product.price}</span>
                </div>
            </div>
            <div class="product-options">
                <div class="size-selector">
                    <label>Size:</label>
                    <select id="size-${product.id}" class="size-select">
                        <option value="s">S</option>
                        <option value="m" selected>M</option>
                        <option value="l">L</option>
                    </select>
                </div>
                <div class="qty-selector">
                    <label>Qty:</label>
                    <input type="number" id="qty-${product.id}" class="qty-input" min="1" value="1">
                </div>
                <button onclick="addToCart(${product.id})" class="add-cart-btn">
                    <span class="btn-icon">🛒</span>
                    <span>Add to Cart</span>
                </button>
            </div>
        </div>
    `;
    }).join('');
}

// ============================================================================
// CART MANAGEMENT
// ============================================================================

function addToCart(productId) {
    const product = PRODUCTS.find(p => p.id === productId);
    if (!product) return;
    
    const size = document.getElementById(`size-${productId}`).value;
    const quantity = parseInt(document.getElementById(`qty-${productId}`).value);
    
    const cartItem = {
        productId: product.id,
        name: product.name,
        design: product.design,
        baseColor: product.baseColor,
        size: size,
        quantity: quantity,
        price: product.price
    };
    
    cart.push(cartItem);
    saveCart();
    renderCart();
    showToast(`✓ ${product.name} added to cart!`, 'success');
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    renderCart();
    showToast('Item removed from cart', 'info');
    
    // Update checkout page if it's open
    if (document.getElementById('checkout-section').style.display === 'block') {
        renderCheckoutItems();
    }
}

function renderCart() {
    const cartItemsEl = document.getElementById('cart-items');
    const cartCountEl = document.getElementById('cart-count');
    const checkoutBtn = document.getElementById('checkout-btn');
    
    cartCountEl.textContent = cart.length;
    
    if (cart.length === 0) {
        cartItemsEl.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
        checkoutBtn.disabled = true;
        return;
    }
    
    checkoutBtn.disabled = false;
    
    cartItemsEl.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <strong>${item.name}</strong>
                <p>${item.design} - ${item.baseColor}</p>
                <p>Size: ${item.size.toUpperCase()} | Qty: ${item.quantity}</p>
            </div>
            <button onclick="removeFromCart(${index})" class="remove-btn">Remove</button>
        </div>
    `).join('');
}

function toggleCart() {
    const sidebar = document.getElementById('cart-sidebar');
    const backdrop = document.getElementById('cart-backdrop');
    sidebar.classList.toggle('open');
    backdrop.classList.toggle('show');
}

function checkout() {
    const token = getAuthToken();
    if (!token) {
        showMessage('Please login first', 'error');
        showLogin();
        return;
    }
    
    if (cart.length === 0) {
        showMessage('Cart is empty', 'error');
        return;
    }
    
    toggleCart();
    showCheckoutPage();
}

function renderCheckoutItems() {
    const checkoutItemsEl = document.getElementById('checkout-items');
    const totalItemsEl = document.getElementById('total-items');
    
    if (cart.length === 0) {
        checkoutItemsEl.innerHTML = '<p>No items in cart</p>';
        totalItemsEl.textContent = '0';
        return;
    }
    
    let totalItems = 0;
    
    checkoutItemsEl.innerHTML = cart.map((item) => {
        totalItems += item.quantity;
        return `
            <div class="checkout-item">
                <div class="checkout-item-info">
                    <strong>${item.name}</strong>
                    <p>${item.design} - ${item.baseColor}</p>
                    <p>Size: ${item.size.toUpperCase()} | Quantity: ${item.quantity}</p>
                    <p class="checkout-item-price">$${item.price} each</p>
                </div>
            </div>
        `;
    }).join('');
    
    totalItemsEl.textContent = totalItems;
}

// ============================================================================
// ORDER MANAGEMENT
// ============================================================================

async function placeOrder() {
    const token = getAuthToken();
    if (!token) {
        showMessage('Please login first', 'error');
        showLogin();
        return;
    }
    
    if (cart.length === 0) {
        showMessage('Cart is empty', 'error');
        return;
    }
    
    const placeOrderBtn = document.getElementById('place-order-btn');
    placeOrderBtn.disabled = true;
    placeOrderBtn.textContent = 'Placing Order...';
    
    try {
        const orderPromises = cart.map(item => 
            fetch(`${API_BASE}/orders`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    shirt_size: item.size,
                    base_color: item.baseColor,
                    attachment: item.design,
                    quantity: item.quantity
                })
            })
        );
        
        const results = await Promise.allSettled(orderPromises);
        const successful = [];
        const failed = [];
        
        for (let i = 0; i < results.length; i++) {
            const result = results[i];
            
            if (result.status === 'fulfilled') {
                const response = result.value;
                try {
                    if (response.ok) {
                        const data = await response.json();
                        if (Array.isArray(data) && data.length > 0 && data[0].id) {
                            successful.push(data[0]);
                        } else if (data && data.id) {
                            successful.push(data);
                        } else {
                            failed.push({ 
                                item: cart[i].name, 
                                error: 'Invalid response format' 
                            });
                        }
                    } else {
                        const errorData = await response.json().catch(() => ({}));
                        failed.push({ 
                            item: cart[i].name, 
                            error: errorData.error || `HTTP ${response.status}` 
                        });
                    }
                } catch (parseError) {
                    failed.push({ 
                        item: cart[i].name, 
                        error: `Failed to parse response: ${response.status}` 
                    });
                    logError('Order Parse', parseError);
                }
            } else {
                failed.push({ 
                    item: cart[i].name, 
                    error: result.reason?.message || 'Request failed' 
                });
            }
        }
        
        if (failed.length === 0 && successful.length === cart.length) {
            showToast('✓ Order placed successfully!', 'success');
            cart = [];
            saveCart();
            renderCart();
            loadOrders();
            
            setTimeout(() => {
                goBackToStore();
            }, 1500);
        } else {
            const errorMsg = failed.length > 0 
                ? `Some items failed: ${failed.map(f => `${f.item}: ${f.error}`).join('; ')}`
                : 'Some items failed to order';
            showMessage(errorMsg, 'error');
            placeOrderBtn.disabled = false;
            placeOrderBtn.textContent = 'Place Order';
        }
    } catch (error) {
        showMessage(`Error placing order: ${error.message || 'Unknown error'}`, 'error');
        placeOrderBtn.disabled = false;
        placeOrderBtn.textContent = 'Place Order';
        logError('Order Placement', error);
    }
}

async function loadOrders() {
    const token = getAuthToken();
    if (!token) return;
    
    try {
        const response = await fetch(`${API_BASE}/orders`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const orders = await response.json();
        const container = document.getElementById('orders-container');
        
        if (orders.length === 0) {
            container.innerHTML = '<p>No orders yet. Place your first order above!</p>';
            return;
        }
        
        container.innerHTML = orders.map(order => `
            <div class="order-item">
                <p><strong>Order #${order.id}</strong></p>
                <p>Size: ${order.shirt_size.toUpperCase()} | Color: ${order.base_color}</p>
                <p>Quantity: ${order.quantity}</p>
                ${order.attachment ? `<p>Design: ${order.attachment}</p>` : ''}
                <p>Created: ${new Date(order.created_at).toLocaleString()}</p>
                <span class="status ${order.status}">${order.status}</span>
            </div>
        `).join('');
    } catch (error) {
        logError('Load Orders', error);
    }
}

// ============================================================================
// AUTHENTICATION
// ============================================================================

async function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch(`${API_BASE}/clients/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                client_name: name,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            saveUserSession(data.token, {
                client_id: data.client_id,
                client_name: data.client_name,
                email: data.email
            });
            showMessage('Registration successful!', 'success');
            showStore(data);
            loadOrders();
        } else {
            showMessage(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        logError('Registration', error);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_BASE}/clients/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            saveUserSession(data.token, {
                client_id: data.client_id,
                client_name: data.client_name,
                email: data.email
            });
            showMessage('Login successful!', 'success');
            showStore(data);
            loadOrders();
        } else {
            showMessage(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        logError('Login', error);
    }
}

function logout() {
    clearUserSession();
    cart = [];
    saveCart();
    showLogin();
    showMessage('Logged out successfully', 'success');
}

// ============================================================================
// INITIALIZATION
// ============================================================================

window.addEventListener('DOMContentLoaded', () => {
    const token = getAuthToken();
    const userInfo = getUserInfo();
    
    if (token && userInfo) {
        showStore(userInfo);
        renderProducts();
        renderCart();
        loadOrders();
    } else {
        showLogin();
    }
});
