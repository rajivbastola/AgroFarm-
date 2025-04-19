import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { addToCart } from '../features/cartSlice.ts';
import { addNotification } from '../features/notificationSlice.ts';
import { productsApi, Product } from '../services/api.ts';
import { useAsync } from '../hooks/useAsync.ts';
import LoadingSpinner from '../components/LoadingSpinner.tsx';
import SearchBar from '../components/SearchBar.tsx';

export default function Products() {
  const {
    data: allProducts = [],
    isLoading,
    error,
    run,
  } = useAsync<Product[]>();
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const dispatch = useDispatch();

  useEffect(() => {
    run(productsApi.getAll().then(response => response.data));
  }, [run]);

  useEffect(() => {
    setFilteredProducts(allProducts);
  }, [allProducts]);

  const handleSearch = (query: string) => {
    const lowercaseQuery = query.toLowerCase();
    const filtered = allProducts.filter(product => 
      product.name.toLowerCase().includes(lowercaseQuery) ||
      product.description.toLowerCase().includes(lowercaseQuery)
    );
    setFilteredProducts(filtered);
  };

  const handleAddToCart = (product: Product) => {
    dispatch(addToCart({
      id: product.id,
      name: product.name,
      price: product.price
    }));
    dispatch(addNotification({
      message: `${product.name} added to cart`,
      type: 'success'
    }));
  };

  if (isLoading) return (
    <div className="flex justify-center items-center min-h-[400px]">
      <LoadingSpinner size="large" />
    </div>
  );
  
  if (error) return (
    <div className="text-center py-12">
      <div className="text-red-600 text-xl mb-4">{error.message}</div>
      <button 
        onClick={() => run(productsApi.getAll().then(response => response.data))}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
      >
        Try Again
      </button>
    </div>
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Our Products</h1>
        <SearchBar 
          onSearch={handleSearch}
          placeholder="Search products..."
        />
      </div>
      
      {filteredProducts.length === 0 ? (
        <div className="text-center py-12 text-gray-600">
          No products found matching your search.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredProducts.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow p-6">
              {product.image_url && (
                <img 
                  src={product.image_url} 
                  alt={product.name}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                />
              )}
              <h2 className="text-xl font-semibold mb-2">{product.name}</h2>
              <p className="text-gray-600 mb-4">{product.description}</p>
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold">${product.price.toFixed(2)}</span>
                <button
                  onClick={() => handleAddToCart(product)}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}