"use client";

import React, { useMemo } from "react";
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

interface PaginationProps {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  isFetching?: boolean;
}

export function Pagination({
  page,
  totalPages,
  onPageChange,
  isFetching = false,
}: PaginationProps) {
  // Memoize page range array calculation
  const pages = useMemo(() => {
    if (totalPages <= 7) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    if (page <= 4) {
      return [1, 2, 3, 4, 5, "...", totalPages];
    }

    if (page >= totalPages - 3) {
      return [1, "...", totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
    }

    return [1, "...", page - 1, page, page + 1, "...", totalPages];
  }, [page, totalPages]);

  if (totalPages <= 1) return null;

  const isPrevDisabled = page <= 1 || isFetching;
  const isNextDisabled = page >= totalPages || isFetching;

  return (
    <nav
      aria-label="Pagination Navigation"
      className="mt-12 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-200 pt-6"
    >
      {/* Page Info */}
      <div className="text-xs font-semibold text-slate-500">
        Page <span className="text-slate-900 font-bold">{page}</span> of{" "}
        <span className="text-slate-900 font-bold">{totalPages}</span>
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center gap-1.5 flex-wrap justify-center">
        {/* First Page */}
        <button
          type="button"
          onClick={() => onPageChange(1)}
          disabled={isPrevDisabled}
          aria-label="Go to first page"
          className="w-9 h-9 rounded-xl border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-300 disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200 disabled:cursor-not-allowed flex items-center justify-center transition-all cursor-pointer shadow-2xs"
        >
          <ChevronsLeft className="w-4 h-4" />
        </button>

        {/* Previous Page */}
        <button
          type="button"
          onClick={() => onPageChange(page - 1)}
          disabled={isPrevDisabled}
          aria-label="Go to previous page"
          className="h-9 px-3 rounded-xl border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-300 disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200 disabled:cursor-not-allowed flex items-center gap-1 text-xs font-bold transition-all cursor-pointer shadow-2xs"
        >
          <ChevronLeft className="w-4 h-4" />
          <span className="hidden sm:inline">Previous</span>
        </button>

        {/* Page Numbers */}
        <div className="flex items-center gap-1">
          {pages.map((p, idx) => {
            if (p === "...") {
              return (
                <span
                  key={`ellipsis-${idx}`}
                  className="w-8 h-9 flex items-center justify-center text-xs font-bold text-slate-400 select-none"
                >
                  •••
                </span>
              );
            }

            const pageNum = p as number;
            const isActive = pageNum === page;

            return (
              <button
                key={pageNum}
                type="button"
                onClick={() => onPageChange(pageNum)}
                disabled={isFetching || isActive}
                aria-label={`Go to page ${pageNum}`}
                aria-current={isActive ? "page" : undefined}
                className={`w-9 h-9 rounded-xl text-xs font-extrabold flex items-center justify-center transition-all cursor-pointer ${
                  isActive
                    ? "bg-[#2563EB] text-white shadow-md shadow-blue-500/20 cursor-default"
                    : "bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 disabled:opacity-50"
                }`}
              >
                {pageNum}
              </button>
            );
          })}
        </div>

        {/* Next Page */}
        <button
          type="button"
          onClick={() => onPageChange(page + 1)}
          disabled={isNextDisabled}
          aria-label="Go to next page"
          className="h-9 px-3 rounded-xl border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-300 disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200 disabled:cursor-not-allowed flex items-center gap-1 text-xs font-bold transition-all cursor-pointer shadow-2xs"
        >
          <span className="hidden sm:inline">Next</span>
          <ChevronRight className="w-4 h-4" />
        </button>

        {/* Last Page */}
        <button
          type="button"
          onClick={() => onPageChange(totalPages)}
          disabled={isNextDisabled}
          aria-label="Go to last page"
          className="w-9 h-9 rounded-xl border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-300 disabled:opacity-40 disabled:hover:bg-white disabled:hover:border-slate-200 disabled:cursor-not-allowed flex items-center justify-center transition-all cursor-pointer shadow-2xs"
        >
          <ChevronsRight className="w-4 h-4" />
        </button>
      </div>
    </nav>
  );
}
