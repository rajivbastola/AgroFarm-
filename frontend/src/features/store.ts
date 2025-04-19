import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import cartReducer from './cartSlice';
import notificationReducer from './notificationSlice.ts';

export const store = configureStore({
  reducer: {
    cart: cartReducer,
    notification: notificationReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;