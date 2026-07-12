"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { ShieldCheck, Smartphone, Store, UserRound } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { useAuth } from "@/hooks/useAuth";

const loginSchema = z.object({
  username: z.string().min(3, "نام کاربری باید حداقل ۳ کاراکتر باشد."),
  password: z.string().min(6, "رمز عبور باید حداقل ۶ کاراکتر باشد."),
});

type LoginFormValues = z.infer<typeof loginSchema>;

const highlights = [
  "مدیریت یکپارچه شعب، موجودی و فروش روزانه",
  "داشبورد لحظه‌ای برای رصد عملکرد فروشگاه",
  "کنترل اقساط، حسابداری و گردش مالی در یک محیط واحد",
];

export default function LoginPage() {
  const router = useRouter();
  const { login, isAuthenticated, isLoading } = useAuth();
  const [submitError, setSubmitError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { username: "", password: "" },
  });

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, isLoading, router]);

  const onSubmit = async (values: LoginFormValues) => {
    try {
      setSubmitError(null);
      await login(values);
      router.push("/dashboard");
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : "ورود با خطا مواجه شد.");
    }
  };

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-10 sm:px-6 lg:px-8">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(79,70,229,0.18),transparent_35%),radial-gradient(circle_at_bottom_left,rgba(14,165,233,0.12),transparent_25%)]" />
      <div className="relative grid w-full max-w-6xl gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <section className="glass-panel hidden min-h-[620px] flex-col justify-between overflow-hidden p-10 lg:flex">
          <div className="space-y-6">
            <div className="inline-flex w-fit items-center gap-3 rounded-full border border-primary/15 bg-primary/5 px-4 py-2 text-sm text-primary">
              <Store className="h-4 w-4" />
              سامانه مدیریت حرفه‌ای فروشگاه موبایل و لوازم جانبی
            </div>
            <div className="space-y-4">
              <h1 className="text-balance text-4xl font-black leading-tight text-slate-900 dark:text-white">فروشگاه شاکار</h1>
              <p className="max-w-xl text-lg leading-8 text-slate-600 dark:text-slate-300">
                بستری یکپارچه برای کنترل فروش، انبار، شعب، حسابداری و گزارشات مدیریتی با طراحی ویژه برای فروشگاه‌های موبایل و لوازم جانبی.
              </p>
            </div>
          </div>
          <div className="grid gap-4">
            {highlights.map((item) => (
              <div key={item} className="flex items-center gap-4 rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-slate-800 dark:bg-slate-900/60">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <p className="text-sm leading-7 text-slate-700 dark:text-slate-300">{item}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="flex items-center justify-center">
          <Card className="w-full max-w-xl border-white/70 bg-white/85 shadow-soft backdrop-blur-xl dark:bg-slate-950/80">
            <CardHeader className="space-y-4 pb-8 text-center">
              <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-primary text-white shadow-lg shadow-primary/25">
                <Smartphone className="h-10 w-10" />
              </div>
              <div className="space-y-2">
                <CardTitle className="text-3xl font-black text-slate-900 dark:text-white">ورود به فروشگاه شاکار</CardTitle>
                <CardDescription className="text-base leading-7">برای دسترسی به پنل مدیریت، نام کاربری و رمز عبور خود را وارد کنید.</CardDescription>
              </div>
            </CardHeader>
            <CardContent>
              <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
                <Input label="نام کاربری" placeholder="مثلاً admin" error={errors.username?.message} leftIcon={<UserRound className="h-4 w-4" />} {...register("username")} />
                <Input label="رمز عبور" type="password" placeholder="رمز عبور خود را وارد کنید" error={errors.password?.message} leftIcon={<ShieldCheck className="h-4 w-4" />} {...register("password")} />

                {submitError ? <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/30 dark:text-red-200">{submitError}</div> : null}

                <Button className="h-12 text-base font-bold" fullWidth isLoading={isSubmitting} type="submit">
                  ورود به سامانه
                </Button>
              </form>

              <div className="mt-8 grid gap-3 rounded-2xl bg-slate-50 p-4 text-sm text-slate-600 dark:bg-slate-900/60 dark:text-slate-300">
                <div className="flex items-center justify-between"><span>امنیت ورود</span><span className="font-semibold text-primary">توکن و نشست امن</span></div>
                <div className="flex items-center justify-between"><span>پشتیبانی</span><span className="font-semibold">داشبورد فارسی و RTL</span></div>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </main>
  );
}
