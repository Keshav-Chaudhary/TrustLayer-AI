import { create } from 'zustand';

interface ChatStore {
  isOpen: boolean;
  activeHotelId: string | null;
  activeHotelName: string | null;
  openChat: (hotelId?: string | null, hotelName?: string | null) => void;
  closeChat: () => void;
  toggleChat: (hotelId?: string | null, hotelName?: string | null) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  isOpen: false,
  activeHotelId: null,
  activeHotelName: null,
  openChat: (hotelId = null, hotelName = null) => set({ isOpen: true, activeHotelId: hotelId, activeHotelName: hotelName }),
  closeChat: () => set({ isOpen: false }),
  toggleChat: (hotelId = null, hotelName = null) => set((state) => ({ 
    isOpen: !state.isOpen, 
    activeHotelId: hotelId !== undefined ? hotelId : state.activeHotelId,
    activeHotelName: hotelName !== undefined ? hotelName : state.activeHotelName
  })),
}));
