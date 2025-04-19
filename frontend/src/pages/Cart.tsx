import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../features/store.ts';
import { removeFromCart, updateQuantity, CartItem } from '../features/cartSlice.ts';
import { addNotification } from '../features/notificationSlice.ts';

export default function Cart() {
  const cartItems = useSelector((state: RootState) => state.cart?.items || []);
  const dispatch = useDispatch();

  const total = cartItems.reduce((sum: number, item: CartItem) => 
    sum + item.price * item.quantity, 0
  );

  const handleQuantityChange = (id: number, quantity: number, name: string) => {
    if (quantity < 1) {
      dispatch(removeFromCart(id));
      dispatch(addNotification({
        message: `${name} removed from cart`,
        type: 'info'
      }));
    } else {
      dispatch(updateQuantity({ id, quantity }));
      dispatch(addNotification({
        message: `${name} quantity updated`,
        type: 'success'
      }));
    }
  };

  const handleRemove = (id: number, name: string) => {
    dispatch(removeFromCart(id));
    dispatch(addNotification({
      message: `${name} removed from cart`,
      type: 'info'
    }));
  };

  if (cartItems.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold mb-4">Your cart is empty</h2>
        <a href="/products" className="text-blue-600 hover:underline">
          Continue Shopping
        </a>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>
      <div className="space-y-4">
        {cartItems.map((item) => (
          <div key={item.id} className="flex items-center justify-between bg-white p-4 rounded-lg shadow">
            <div>
              <h3 className="text-lg font-semibold">{item.name}</h3>
              <p className="text-gray-600">${item.price}</p>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center">
                <button 
                  onClick={() => handleQuantityChange(item.id, item.quantity - 1, item.name)}
                  className="px-3 py-1 bg-gray-200 rounded-l hover:bg-gray-300"
                >
                  -
                </button>
                <span className="px-4 py-1 bg-gray-100">{item.quantity}</span>
                <button 
                  onClick={() => handleQuantityChange(item.id, item.quantity + 1, item.name)}
                  className="px-3 py-1 bg-gray-200 rounded-r hover:bg-gray-300"
                >
                  +
                </button>
              </div>
              
              <button 
                onClick={() => handleRemove(item.id, item.name)}
                className="text-red-600 hover:text-red-800"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
        
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between items-center text-xl font-semibold">
            <span>Total:</span>
            <span>${total.toFixed(2)}</span>
          </div>
          <button 
            onClick={() => {
              dispatch(addNotification({
                message: 'This is a demo - checkout not implemented',
                type: 'info'
              }));
            }}
            className="w-full mt-4 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700"
          >
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
}