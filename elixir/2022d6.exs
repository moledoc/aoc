defmodule Solution do
  def loop([_a1, _a2, _a3], _idx) do
    -1
  end

  def loop(x, idx, marker) do
    l =
      x
      |> Enum.take(marker)
      |> Enum.uniq()
      |> length

    cond do
      l == marker -> idx + marker
      true -> loop(Enum.drop(x, 1), idx + 1, marker)
    end
  end

  def ex1(filename) do
    File.read!(filename)
    |> String.trim("\n")
    |> String.graphemes()
    |> loop(0, 4)
  end

  def ex2(filename) do
    File.read!(filename)
    |> String.trim("\n")
    |> String.graphemes()
    |> loop(0, 14)
  end
end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
