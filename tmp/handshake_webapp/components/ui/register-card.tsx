"use client";

import { useState } from "react";
import { useDomesticAnimate, ANIMATION_CLASSES } from "@/lib/domestic-animate";
import { cn } from "@/lib/utils";

export function RegisterCard() {
  const ref = useRef<HTMLFormElement | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  useDomesticAnimate(ref, { duration: 600, classNames: [ANIMATION_CLASSES["a-visible"]] });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Please enter your name.");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }
    setError("");
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div ref={ref} className="card-interactive p-8 text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-600">
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
        </div>
        <h2 className="mt-4 text-xl font-semibold text-gray-900">You're on the list</h2>
        <p className="mt-2 text-sm text-gray-600">We'll be in touch soon with next steps.</p>
      </div>
    );
  }

  return (
    <div ref={ref} className="card-interactive p-6">
      <h2 className="text-xl font-semibold text-gray-900">Create your account</h2>
      <p className="mt-1 text-sm text-gray-500">Join to save your profile and get personalized recommendations.</p>

      <form onSubmit={handleSubmit} className="mt-5 space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full name</label>
          <input
            id="name"
            type="text"
            className="input mt-1"
            placeholder="Jane Doe"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            type="email"
            className="input mt-1"
            placeholder="jane@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          type="submit"
          className="btn btn-primary w-full"
        >
          Sign up
        </button>
        <p className="text-xs text-gray-400 text-center">By signing up you agree to our terms and privacy policy.</p>
      </form>
    </div>
  );
}

import { useRef } from "react";
