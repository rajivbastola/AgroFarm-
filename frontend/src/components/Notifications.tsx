import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { removeNotification } from '../features/notificationSlice';

export default function Notifications() {
  const dispatch = useDispatch();
  const notifications = useSelector((state: RootState) => state.notification.notifications);

  useEffect(() => {
    notifications.forEach(notification => {
      const duration = notification.duration || 5000;
      if (notification.id) {
        setTimeout(() => {
          dispatch(removeNotification(notification.id!));
        }, duration);
      }
    });
  }, [notifications, dispatch]);

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map(notification => (
        <div
          key={notification.id}
          className={`px-4 py-2 rounded-lg shadow-lg ${
            notification.type === 'success'
              ? 'bg-green-500'
              : notification.type === 'error'
              ? 'bg-red-500'
              : notification.type === 'warning'
              ? 'bg-yellow-500'
              : 'bg-blue-500'
          } text-white`}
        >
          {notification.message}
        </div>
      ))}
    </div>
  );
}