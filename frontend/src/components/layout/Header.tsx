import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { RootState } from '../../features/store.ts';
import type { CartItem } from '../../features/cartSlice.ts';
import { useAuth } from '../../contexts/AuthContext.tsx';

export default function Header() {
  const cartItems = useSelector((state: RootState) => state.cart?.items || []);
  const itemCount = cartItems.reduce((sum: number, item: CartItem) => 
    sum + item.quantity, 0
  );
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white shadow">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-xl font-bold">E-Commerce</Link>
          
          <div className="flex gap-6 items-center">
            <Link to="/products" className="hover:text-blue-600">Products</Link>
            <Link to="/cart" className="flex items-center hover:text-blue-600">
              Cart {itemCount > 0 && 
                <span className="ml-1 bg-blue-600 text-white rounded-full px-2 py-1 text-xs">
                  {itemCount}
                </span>
              }
            </Link>
            {isAuthenticated ? (
              <button 
                onClick={logout}
                className="hover:text-blue-600"
              >
                Logout
              </button>
            ) : (
              <Link to="/auth" className="hover:text-blue-600">Login</Link>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}