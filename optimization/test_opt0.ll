; ModuleID = 'test.c'
source_filename = "test.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.13.0"

@main.mem = private unnamed_addr constant [2 x i32] [i32 -1, i32 -1], align 4
@.str = private unnamed_addr constant [13 x i8] c"Result = %d\0A\00", align 1

; Function Attrs: noinline nounwind ssp uwtable
define i32 @main(i32, i8**) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i8**, align 8
  %5 = alloca [2 x i32], align 4
  %6 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  store i8** %1, i8*** %4, align 8
  %7 = bitcast [2 x i32]* %5 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* bitcast ([2 x i32]* @main.mem to i8*), i64 8, i32 4, i1 false)
  store i32 2, i32* %6, align 4
  %8 = load i32, i32* %6, align 4
  %9 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  store i32 %8, i32* %9, align 4
  %10 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %11 = load i32, i32* %10, align 4
  store i32 %11, i32* %6, align 4
  %12 = load i32, i32* %6, align 4
  %13 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %14 = load i32, i32* %13, align 4
  %15 = add nsw i32 %12, %14
  store i32 %15, i32* %6, align 4
  %16 = load i32, i32* %6, align 4
  %17 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  store i32 %16, i32* %17, align 4
  %18 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  %19 = load i32, i32* %18, align 4
  store i32 %19, i32* %6, align 4
  %20 = load i32, i32* %6, align 4
  %21 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %22 = load i32, i32* %21, align 4
  %23 = add nsw i32 %20, %22
  store i32 %23, i32* %6, align 4
  %24 = load i32, i32* %6, align 4
  %25 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  store i32 %24, i32* %25, align 4
  %26 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %27 = load i32, i32* %26, align 4
  store i32 %27, i32* %6, align 4
  %28 = load i32, i32* %6, align 4
  %29 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  %30 = load i32, i32* %29, align 4
  %31 = add nsw i32 %28, %30
  store i32 %31, i32* %6, align 4
  %32 = load i32, i32* %6, align 4
  %33 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  store i32 %32, i32* %33, align 4
  %34 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  %35 = load i32, i32* %34, align 4
  store i32 %35, i32* %6, align 4
  %36 = load i32, i32* %6, align 4
  %37 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %38 = load i32, i32* %37, align 4
  %39 = add nsw i32 %36, %38
  store i32 %39, i32* %6, align 4
  %40 = load i32, i32* %6, align 4
  %41 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  store i32 %40, i32* %41, align 4
  %42 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %43 = load i32, i32* %42, align 4
  store i32 %43, i32* %6, align 4
  %44 = load i32, i32* %6, align 4
  %45 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @.str, i32 0, i32 0), i32 %44)
  ret i32 0
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #1

declare i32 @printf(i8*, ...) #2

attributes #0 = { noinline nounwind ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"PIC Level", i32 2}
!1 = !{!"Apple LLVM version 9.0.0 (clang-900.0.38)"}
