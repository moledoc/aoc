defmodule Solution do
  def ex1(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(fn x -> String.split(x, ",") end)
    |> Enum.reduce(0, fn [a1, a2], acc ->
      # |> dbg
      [a1_l, a1_u] = String.split(a1, "-") |> Enum.map(fn x -> String.to_integer(x) end)
      # |> dbg
      [a2_l, a2_u] = String.split(a2, "-") |> Enum.map(fn x -> String.to_integer(x) end)

      cond do
        a1_l <= a2_l and a2_u <= a1_u -> acc + 1
        a2_l <= a1_l and a1_u <= a2_u -> acc + 1
        true -> acc + 0
      end

      # |> dbg
    end)
  end

  def ex2(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(fn x -> String.split(x, ",") end)
    |> Enum.reduce(0, fn [a1, a2], acc ->
      # |> dbg
      [a1_l, a1_u] = String.split(a1, "-") |> Enum.map(fn x -> String.to_integer(x) end)
      # |> dbg
      [a2_l, a2_u] = String.split(a2, "-") |> Enum.map(fn x -> String.to_integer(x) end)

      cond do
        # a2 in a1
        a1_l <= a2_l and a2_u <= a1_u -> acc + 1
        a2_l <= a1_l and a1_u <= a2_u -> acc + 1
        # a2_l in a1
        a1_l <= a2_l and a2_l <= a1_u -> acc + 1
        # a2_u in a1
        a1_l <= a2_u and a2_u <= a1_u -> acc + 1
        # a1_l in a2
        a2_l <= a1_l and a1_l <= a2_u -> acc + 1
        # a1_u in a2
        a2_l <= a1_u and a1_u <= a2_u -> acc + 1
        true -> acc + 0
      end

      # |> dbg
    end)
  end
end

IO.write("ex1: #{inspect(Solution.ex1("input.txt"))}\n")
IO.write("ex2: #{inspect(Solution.ex2("input.txt"))}\n")
